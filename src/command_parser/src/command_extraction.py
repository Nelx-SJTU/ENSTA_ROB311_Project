#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
import spacy

nlp = spacy.load("en_core_web_sm")

object_mapping = {
    "book": 1,
    "flask": 2,
    "jar": 3,
    "container": 4
}

left_relations = {
    3: 2, 
    4: 3, 
    2: 1  
}

right_relations = {
    1: 2,  
    2: 3,  
    3: 4  
}

publisher = rospy.Publisher('task_name', String, queue_size=10)


def parse_command(command):
    """Parse a command and extract structured information."""
    result = {
        'objectA': None,
        'action': None,
        'objectB': None,
        'objectC': None,
        'direction': None
    }
    doc = nlp(unicode(command)) 
    #print("Raw input: {}, Unicode: {}".format(command, repr(command)))


   # for token in doc:
     #   print("Token: {}, Lemma: {}, POS: {}, Dep: {}, Head: {}".format(token.text, token.lemma_, token.pos_, token.dep_, token.head.text))



    for token in doc:
        if token.lemma_ == "move":
            result['action'] = token.text
            for child in token.children:
                if child.dep_ == "dobj":
                    result['objectA'] = child.text
                elif child.dep_ == "prep" and child.text == "to":
                    for grandchild in child.children:
                        if grandchild.dep_ == "pobj" and grandchild.text in ["left", "right"]:
                            result['direction'] = grandchild.text
                            for subchild in grandchild.children:
                                if subchild.dep_ == "prep" and subchild.text == "of":
                                    for subsubchild in subchild.children:
                                        if subsubchild.dep_ == "pobj":
                                            result['objectB'] = subsubchild.text
            for token in doc:
                if token.dep_ == "prep" and token.text == "between":
                    result['direction'] = "between"
                    object_list = []
                    for obj in token.children:
                        if obj.dep_ == "pobj":
                            object_list.append(obj.text)
                            for conj_obj in obj.conjuncts:
                                object_list.append(conj_obj.text)
                        elif obj.dep_ == "conj":
                            object_list.append(obj.text)
                    if len(object_list) >= 2:
                        result['objectB'] = object_list[0]
                        result['objectC'] = object_list[1]
    return result

def construct_task_message(parsed_result):
    """Construct the task_name message based on parsed results."""
    objectA = parsed_result.get('objectA').lower()
    objectB = parsed_result.get('objectB').lower()
    direction = parsed_result.get('direction')

    if not objectA or not objectB or not direction:
        rospy.logwarn("Incomplete command: {}".format(parsed_result))
        return None

    id_A = object_mapping.get(objectA)
    id_B = object_mapping.get(objectB)

    if not id_A or not id_B:
        rospy.logwarn("Unknown objects in command: {}, {}".format(objectA, objectB))
        rospy.logdebug("Current object_mapping: {}".format(object_mapping))
        return None

    if direction == "left":
        id_B = left_relations.get(id_B, id_B)  
    elif direction == "right":
        id_B = right_relations.get(id_B, id_B) 
    else:
        rospy.logwarn("Unsupported direction: {}".format(direction))
        return None

    task_message = "{}_to_{}".format(id_A, id_B)
    return task_message




def command_callback(msg):
    rospy.loginfo("Received command: {}".format(msg.data))
    parsed_result = parse_command(msg.data)
    rospy.loginfo("Parsed result: {}".format(parsed_result))

    task_message = construct_task_message(parsed_result)
    if task_message:
        rospy.loginfo("Publishing task message: {}".format(task_message))
        publisher.publish(task_message)


def command_parser_node():
    rospy.init_node('command_parser_node', anonymous=True)
    rospy.Subscriber('recognized_speech', String, command_callback)
    rospy.loginfo("Command parser node started. Waiting for commands...")
    rospy.spin()

if __name__ == '__main__':
    try:
        command_parser_node()
    except rospy.ROSInterruptException:
        pass