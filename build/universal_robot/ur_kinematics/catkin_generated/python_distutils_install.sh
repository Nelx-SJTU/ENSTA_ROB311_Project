#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/catkin_ws/ENSTA_ROB311_Project/src/universal_robot/ur_kinematics"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/catkin_ws/ENSTA_ROB311_Project/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/catkin_ws/ENSTA_ROB311_Project/install/lib/python2.7/dist-packages:/catkin_ws/ENSTA_ROB311_Project/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/catkin_ws/ENSTA_ROB311_Project/build" \
    "/usr/bin/python2" \
    "/catkin_ws/ENSTA_ROB311_Project/src/universal_robot/ur_kinematics/setup.py" \
     \
    build --build-base "/catkin_ws/ENSTA_ROB311_Project/build/universal_robot/ur_kinematics" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/catkin_ws/ENSTA_ROB311_Project/install" --install-scripts="/catkin_ws/ENSTA_ROB311_Project/install/bin"
