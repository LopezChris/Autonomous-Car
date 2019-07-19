# Tutorial 3: AI to the edge

We will use Cloudera Data Platform to have access car data in Hadoop - HDFS for when we work in Cloudera Data Science Workbench (CDSW) and train the Keras CNN model. This access to HDFS will also allow us to save the model into HDFS from CDSW. CDSW will be running on the same ec2 instance as CDH and HDFS, but in a docker container.

Download the source code to train the model to your local computer

~~~bash
wget https://raw.githubusercontent.com/james94/Autonomous-Car/master/documentation/assets/src/hdfs-train.zip
~~~

now open an instance of Cloudera Data Science Workbench

- CDSW runs at web address:

 `http://cdsw.<cdp-public-cloud-dns>.nip.io`

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

continue to wait until all of the files that were stored on the edge device have been moved to HDFS. Once all of the files have been moved and you have installed all of the dependencies you are ready to begin training

![deps](./documentation/assets/images/tutorial3/deps.jpg)

Now select the `hdfs-model.py` file and select `Run>Run All` your training should look like this

![training](./documentation/assets/images/tutorial3/training.jpg)

for more details about how the training works check out this [blog](link)

### Back to the Edge

Once all of the data that was stored on our "Edge" device is transfered to HDFS we can begin training

Now that you have a model stored on HDFS we can move it back to the edge to complete the cycle. Navigate to NiFi UI and create a new `GetHDFS` processor and connect it to an **output** port

Update the following processor properties:

| Property  | Value  |
|:---|---:|
| `Hadoop Configuration Resources` | `/tmp/service/hdfs/core-site.xml` |
| `Directory`  | `/tmp/csdv/data/output/model/`  |

your NiFi canvas should look like this

![gethdfs](./documentation/assets/images/tutorial3/gethdfs.jpg)

Now navigate to CEM UI and lay out a new RPG

Add URL NiFi is running on:

| Setting  | Value  |
|:---|---:|
| `URL` | `http://<nifi-public-DNS>:8080/nifi/` |

connect the RPG to a new `PutFile` processor and name it **GetModel**

Connect the new RPG to the processor, then add the NiFi origin input port ID you want to send the csv data:

| Settings  | Value  |
|:---|---:|
| `Source Input Port ID` | `<NiFi-input-port-ID>` |

once you are finished your flow should look like this

![minifiedge](./documentation/assets/images/tutorial3/minifi-edge.jpg)

[Insert image of model back into car]()

## Conclusion