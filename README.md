# Action Recognition Toy

A Demo Project action recognition.

## Module List

- iOS app with Xcode
- tf-pose-v2
- MS_G3D



## iOS App Demo

wait to update..





## tf-pose

Originally it is a tensorflow_v1 version of [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose.git), see [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation.git).

We upgraded it to tensorflow v2.

Here is some upgrade details:

- Git clone the tf-pose repository

- Use `upgrade_v2 --intree tf-pose-estimation --outtree tf_pose` to automatically upgrade code of the .py file in the directory from tf1.0 to tf2.0

- Still need some manual tune:

  - add `sys.path.join('..’)` to fix the import problems within the file (e.g. Error occured when use `from tf_pose...`)

  - Delete `tf.contrib` things in the code
  - Comment out the `pycocotools` in eval.py
  - Change `tensorflow.contrib.slim` to `import tf_slim as slim`, NEED to install [tf-slim](https://github.com/google-research/tf-slim.git) : `pip3 install --upgrade tf_slim` 



### Other Notes

- Already used `swig` to generate the Python Interface for the C++ code in pafprocess file. If you want to generate yourself, try to install swig and do `swig -python -c++ pafprocess.i && python3 setup.py build_ext —inplace` in [tf-pose-estimator](https://github.com/ildoonet/tf-pose-estimation.git)’s origin pafprocess directory.





## MS_G3D

Here we use [MS-G3D](https://github.com/kenziyuliu/MS-G3D.git) to further process data from tf-pose.

Many thans to Ziyu Liu for the patient guidance!

Here the MS_G3D file is a *lite* version of the original MS-G3D repository. Deleted some file that don’t need to use, and add the prediction method in pred.py.



### Other Notes 

App.py is the interface in iOS app. Put it here for testing.