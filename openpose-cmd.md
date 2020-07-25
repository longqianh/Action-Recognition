```python
!sudo apt-get install libllvm-7-ocaml-dev libllvm7 llvm-7 llvm-7-dev llvm-7-doc llvm-7-examples llvm-7-runtime

!export LLVM_CONFIG=/usr/bin/llvm-config-7

!git clone https://www.github.com/ildoonet/tf-pose-estimation
  
cd tf-pose-estimation/

ls （可以查看当前文件夹的目录）

!pip3 install -r requirements.txt

! apt-get install swig

cd tf_pose/pafprocess

!swig -python -c++ pafprocess.i && python3 setup.py build_ext --inplace

!git clone https://www.github.com/ildoonet/tf-pose-estimation
  
cd tf-pose-estimation

!python setup.py install

cd models/graph/cmu

!bash download.sh



cd

cd tf-pose-estimation/

pip uninstall tensorflow

pip install tensorflow==1.14.0

!python run.py --model=mobilenet_thin --resize=432x368 --image=/root/tf-pose-estimation/images/p1.jpg

```

