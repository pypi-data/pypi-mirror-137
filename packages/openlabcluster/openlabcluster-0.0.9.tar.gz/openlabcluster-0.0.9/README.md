# DeepLabCluster

## Usage
### Installation

Create a new enviornment with conda enviornment
	
	conda create --name OpenLabCluster
	conda activate OpenLabCluster
	conda install pip
	pip install -r requirements.txt
	
Create a conda enviornment in **Mac-OS**
	
	conda env create -f env-mac2.yml
	conda activate openlabcluster-v2
	conda install python.app
	
   	

### Initialize the User Interface
Go to the file directory and set up python directory

	cd filedirectory/IC_GUI
	export PYTHONPATH=/filedirectory/IC_GUI/

Launch the GUI
	
	python ./openlabcluster/gui/launch_script.py
		
### Run a Demo

#### Create Demo Project
1. Go to *openlabcluster example* folder run 
		
		python3 prepare_video_list.py
2. Launch GUI
3. Set Project Name: e.g., demo
4. Click *Load Preprocessed Keypoints*, choose datafile: */openlabcluster example/demo_data.h5*
5. Click *Choose Training Video List*, choose the file: *./openlabcluster example/video_name.text*
6. Uncheck *Check to use GPU*, if GPU is not avaliable.
7. Set feature Length = 16
8. Click *ok* to create the project

#### Start the Demo Project
1. Go to **Manage Project** panel, 
2. hoose *Load Project*
3. Select config file *filedirectory/IC_GUI/openlabcluster/gui/i-2021-02-16/config.yaml*
4. Cliick **ok**

#### Cluster with Unsupervised Training
1. Click **go to action recognition** to go to active selection and semi-supervised training part.

#### Interative Action Recognition: Labeling Samples and Traing Action Recognition

## Explanation
### Manage Project (Start a New Project or Load Earlier Project)
#### Start a New Project
1. Project Name - name for the project
2.  If you just have videos, use DeepLabCut to extract keypoints. If you already have DeepLabCut-like formatted files, select them with "Load Keypoints Data"
3. Select your videos with "Choose Training Videos List". There should be one video for each keypoint file. Make sure the videos and keypoints files are in the same order.
4. Optionally set a directory for the project to be created (the default is the working directory of this project).
5. Keep the box checked if you have a GPU in your computer you would like to use to train the model.
6. Enter the feature length (number of body parts * number of dimensions per body part, i.e. (x,y) -> 2).
7. Press "Okay", then "Okay" again on the pop up box to create the project.
8. If you would like to edit the config (i.e. change class names, change video cropping), press "Edit Config File"

#### Load Earlier project
1. Select config.yaml file, generated when you create a new project
2. Press "OK", then "Okay" again on the pop up box to launch the project.


### Cluster Data (Form Data into Clusters with Unsupervised Learning)
#### Set the Training Parameters
1. Update Cluster Map Every (Epochs): this helps you to decide when to update the Cluster Map, e.g. set 1 to update Cluster Map every training epoch, set to 5, update every 5 epoch.
2. Save Cluster Map Every (Epochs): this decides when to save Cluster Maps, e.g. if it is 1, update the Cluster Map every training epoch.
3. Maximum Epochs: the number of epoches perform training.
4. Cluster Map Dimension: you can choose "2d" or "3d", if it is "2d" the Cluster Map will be shown in 2D dimension, otherwise it is 3D dimension.
5. Dimension Reduction Methods: possible choices are "PCA", "tSNE", "UMAP". The GUI will use the choosen reduction method to perform dimension reduction and show results in Cluster Map.


#### Buttons
After setting the parameters you can perform analysis:

1. Start Clustering: perform unsupervised sequence regneration task.
2. Continue Clustering: if you stopped the clustering at some stage and want to perform clustering with ealier clustering results, click this button.
3. Stop clustering: usually the clustering will stop when it reaches the maximum epochs, but if you want to stop at itermediate stage, click this button.
4. Reset: Reset the earlier defined trainign parameters to default.
5. Go to Action Recognition: after the unsupervised clustering we go to the next step which includes: i) sample labeling suggestion, ii) sample laebling and iii) semi-supervised action recognition training with labeled samples.

### Iterative Action Recognition
#### Set the Training Parameters
1. Seletction Method: In this part, your selection will decide which method GUI use to select samples for annotation. there are four possible choices ("Cluster Center", "Cluster Random", "Cluster Uncertainty", "Unifrom").
2. \# Samples per Selection: how many samples you want to label in current selection stage.
3. Maimum Epochs: when perform the action recogntion, the maximum epoch the netwrok will be trained.
4. Cluster Map Dimension: you can choose "2d" or "3d", if it is "2d" the Cluster Map will be shown in 2D dimension, otherwise it is 3D dimension.
5. Dimension Reduction Methods: possible choices are "PCA", "tSNE", "UMAP". The GUI will use the choosen reduction method to perform dimension reduction and show results in Cluster Map.

#### Plots
1. Cluter Map Plot:
	
	* The will be dots in different color in the Cluter Map plot.
Red: current sample for labeling and its corresponding video is shown on the rigth.
Blue: the suggested samples for labling in this iteration.
Green: samples already been labeled.
	
	* Zoom: zoom in or zoom out the plot
	
	* Pan: move the plot around.
	
	* Update selection: save the suggeted sample id and start labeling
	
2. Video Plot:
	
	* left panal: show corresponding video for the sample in red color shown in Cluster Map
	
	* right panel: the class name and class id, according to the video, select the class.
	
	* Previous: load the previous video
	
	* Play: paly the video
	
	* next: go to the next video 

3. Buttons:
	
	* perform Action Recognition: save labeling results and train action recognition model.
	
	* Stop Action Recognition: stop training
	
	* Next Seelction: go the next iteration of label selection, labeling and training.
	
	* Get Results: get the prediction from trained model on unlabeled samples. 


