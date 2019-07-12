
## Tutorial 3: Train CNN Model in Cloud

We will use Cloudera Distribution Hadoop (CDH) to have access car data in Hadoop - HDFS for when we work in Cloudera Data Science Workbench (CDSW) and train the Keras CNN model. This access to HDFS will also allow us to save the model into HDFS from CDSW. CDSW will be running on the same ec2 instance as CDH and HDFS, but in a docker container.

- Cloudera Data Science Workbench runs at web address:

 `http://cdsw.<cdh-ec2-public-dns>.nip.io`

Sign in to CDSW and select new project and name it CSDV

![cdsw-ui](./documentation/assets/images/tutorial3/cdsw-ui.jpg)

then select a local folder and upload the CSDV project you downloaded earlier:

![new-project-cdsw](./documentation/assets/images/tutorial3/new-project-cdsw.jpg)

Once the folder uploads to CDSW, open a new workbench:

![openwb](./documentation/assets/images/tutorial3/openwb.jpg)

when selecting to open a new workbench ensure that you have an engine configuration with at least 20Gb of RAM or a GPU with 8GB of RAM and Python3

![openwb](./documentation/assets/images/tutorial3/engine.jpg)

when you start the session click on the read me file and ensure the packages listed there are running in your CDSW engine

![rundep](./documentation/assets/images/tutorial3/run-dep.jpg)

now we can begin training our model, select the `hdfs-model.py` file on the CDSW file explorer, but before we can run the training script we must ensure that there is data flowing in to HDFS from our CEM cluster

enter the following command on the workbench:

`!hdfs dfs -ls /tmp/csdv/data/input/racetrack/image/logitech`

the output should show a few files stored into HDFS. However, if not all of the files you intended to send over are stored into HDFS yet, you should wait because the more data we have the better the model will be.

![dataflowing](./documentation/assets/images/tutorial3/dataflowing.jpg)