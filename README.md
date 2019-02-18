# Exercise set 4: Exercise 3

This project requires the following software to be installed:

* Python 3.7.1

The solution was tested only for the described configurations. Currect work with other configurations is not guaranteed.

Installation includes the fllowing steps:
1. In git repository folder run the following command to initiate virtual environment:

```bash
python3 -m venv venv
```

2. Activate virtual environment by running:

```bash
venv\Scripts\activate
```

3. If everything is done correctly you should see *(venv)* in the beginning of the console line.

4. Install all required Python packages. This requires switching to folder Question3 (it is subfolder of repository folder) and running:

```bash
pip install -r packages.txt
```

## Configuring AWS access

To allow this solution to connect to AWS you should create a folder *.aws* in your user folder. In Windows it will be (typically): *C:\Users\<your user name>*. In UNIX-based system it is enough to run:

```bash
cd ~/
mkdir .aws
```
Then, in this folder it is required to create a file named *credentials*. This file should have the following content:

```
[default]
aws_access_key_id=<your AWS access key>
aws_secret_access_key=<your AWS secret access key>
aws_session_token=<your AWS session token>
```

According to AWS SDK documentation session token is optional, but I had to provide it (otherwise the solution did not work). This file configures API keys to make SDK working. It is also possible to provide API keys directly in the code, but such option does not suite for storing the code into a repository.

After this you need to create a file called *config* in *.aws* folder. This file should have the following content:

```
[default]
region=us-east-1
```

This is required as bucket is located in regison us-east-1 and the region is not specified in the code (so the application can be used in any region without changing its code).

Now, the application is ready for usage.

## Running the application

To run the application it is required to start virtual environment first. To do that run the following command in repository folder:

```bash
venv\Scripts\activate
```

And then:

```bash
python exercise4-backup.py
```

## Functionality

The main idea of this application is to download a certain version of a file from AWS bucket. AWS bucket is predefined and cn not be changed. When the applicaton starts it offers a set of commands:

1. *list*: lists all files in the bucket;
1. *backup*: this command asks a user to select a file and then puts it to the bucket;
1. *versions*: this command aksk a user for a key designating a file in the bucket and then lists all versions of this file. All versions have numbers. Number 1 means the earliest version of the file.
1. *download*: downloads a given version of the file (version and file should be provided by user).
1. *delete*: deletes a given version of the file (version and file should be provided by user).
1. *exit*: stops the application.