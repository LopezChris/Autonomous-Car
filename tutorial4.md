
## Tutorial 4: Deploy Keras Model to Edge

With the model saved in HDFS, we will use NiFi to pull in the model to the dataflow, so it can be transported to the MiNiFi agent running on the edge.

- Jetson TX2 runs at static IP address: `<tx2-static-ip>`

You will need to setup a static IP address.
