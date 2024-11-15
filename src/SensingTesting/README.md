Folder containing ROS and Teensie code to detect and sort Astral Materials

Sort queue logic: sort/detection

two queues: one for unsorted objects and one for the sorted objects

Queue one: when ir sensor reads a new object it is added to unsorted queue

Queue two: when hall effect sensor reads magnetism dequeue from unsorted and add one mag to sorted

Queue two: if magnetism is not detected then either wait until timeout and read as nonmag or wait until new ir read to and if no magnetism is detected then read as nonmag to sorted queue
