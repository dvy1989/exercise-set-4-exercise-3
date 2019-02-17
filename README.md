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

According to AWS SDK documentation session token is optional, but I had to provide it (otherwise the solution did not work).

After this you need to create a file called *config* in *.aws* folder. This file should have the following content:

```
[default]
region=us-east-1
```

Now, the application is ready for usage.