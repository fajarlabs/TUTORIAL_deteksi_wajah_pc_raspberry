# Install Dependencies
sudo apt install cmake build-essential pkg-config git <br />
sudo apt install libjpeg-dev libtiff-dev libjasper-dev libpng-dev libwebp-dev libopenexr-dev <br />
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libdc1394-22-dev libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev <br />
sudo apt install libgtk-3-dev libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5 <br />
sudo apt install libatlas-base-dev liblapacke-dev gfortran <br />
sudo apt install libhdf5-dev libhdf5-103 <br />
sudo apt install python3-dev python3-pip python3-numpy <br />
<br />
<b>Alternatif install OPENCV</b><br />
sudo pip install opencv-contrib-python<br />

<b> Alternatif instalasi tanpa pip opencv-contrib-python</b><br />
sudo nano /etc/dphys-swapfile<br />
Ubah <b>CONF_SWAPSIZE=100 </b> menjadi <b>CONF_SWAPSIZE=2048 </b><br />
Restart swabfile <b>sudo systemctl restart dphys-swapfile</b><br />
<br/>
<b>Cloning OPENCV</b><br />
git clone https://github.com/opencv/opencv.git<br />
git clone https://github.com/opencv/opencv_contrib.git<br /><br />

cmake -D CMAKE_BUILD_TYPE=RELEASE \<br />
-D CMAKE_INSTALL_PREFIX=/usr/local \<br />
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \<br />
-D ENABLE_NEON=ON \<br />
-D ENABLE_VFPV3=ON \<br />
-D BUILD_TESTS=OFF \<br />
-D INSTALL_PYTHON_EXAMPLES=OFF \<br />	
-D OPENCV_ENABLE_NONFREE=ON \<br />
-D CMAKE_SHARED_LINKER_FLAGS=-latomic \<br />
-D BUILD_EXAMPLES=OFF ..<br />

<br />
make -j$(nproc) (proses ini memakan waktu 1 jam lebih )<br />
sudo make install <br />
sudo ldconfig <br />
<br />

Setelah proses diatas selesai kembalikan swabfile seperti semula : <br />
sudo nano /etc/dphys-swapfile (ubah 2048 menjadi 100) nilai dari CONF_SWAPSIZE <br />
<br />
<b> Restart SwabFile service </b> <br />
sudo systemctl restart dphys-swapfile <br />
<br />

Instal library facerecognition :<br />
pip install face-recognition <br />
Install library imutils:<br />
pip install imutils<br />
<br />
Jika ada permasalahan ada pada dlib install by source code seperti langkah-langkah di bawah ini : <br />
$ git clone https://github.com/davisking/dlib.git <br />
$ cd dlib<br />
$ mkdir build<br />
$ cd build <br />
$ cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1<br />
$ cmake --build .<br />
$ cd ..<br />
$ python setup.py install --set USE_AVX_INSTRUCTIONS=1 --set DLIB_USE_CUDA=1 --no DLIB_GIF_SUPPORT <Br />

referensi install opencv : https://yunusmuhammad007.medium.com/2-raspberry-pi-install-opencv-pada-python-3-7-menggunakan-pip3-a2504dffd984
problem gtk2.0 dependency : https://programmersought.com/article/57453207651/

Mulai cloning programnya disini : <b> git clone 
