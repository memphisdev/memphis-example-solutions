# Setting up Memphis
The first step in running the CDC example solution is to start and configure an instance of [Memphis.dev](https://github.com/memphisdev/memphis).

## Running the Memphis.dev Services
The easiest way to run Memphis.dev locally is with the Docker Compose configuration.

1. Check out the repository:
   ```bash
   $ git clone https://github.com/memphisdev/memphis-docker.git
   ```
1. Start the Memphis.dev services:
   ```bash
   $ cd memphis-docker
   $ docker compose up -d
   ```

## Setting up a Station and User
In Memphis.dev, topics are called "stations".  When Memphis.dev is run for the first time, the web UI provides a wizard for creating your first station and user.

1. Point your browser to [http://localhost:9000](http://localhost:9000/).  Click "Sign in with root" at the bottom.
   ![Memphis.dev UI start page](memphis_ui_first_page.png)
1. Log in with the username "root" and the password "memphis"
   ![Memphis.dev UI root login](memphis_ui_login_root.png)
1. Create your first station.  Enter the station name as "todo-cdc-events".  Leave the other settings at their defaults and click the "Next" button in the bottom right.
   ![Memphis.dev UI wizard create station page](memphis_ui_create_station.png)
1. Create your first user.  Use the "todocdcservice" as the username and password.  Click the "Next" button in the bottom right.
   ![Memphis.dev UI wizard create user page](memphis_ui_create_user.png)
1. Click "Next" button on the producer and consumer example screens and finalize the creation.
1. You will be forwarded to the details screen for the new "todo-cdc-events" station.
   ![Memphis.dev UI station overview page](memphis_ui_station_details.png)

## Testing the Memphis.dev Configuration
Example producer and consumer Python scripts are provided to test your setup.

### Start the Consumer
1. Open a terminal to run the consumer
1. Navigate to `../memphis-setup-testing`.
1. Create a Python virtual environment
   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate
   (venv) $
   ```
1. Update pip
   ```bash
   (venv) $ pip install -U pip wheel
   ```
1. Install the dependencies
   ```bash
   (venv) $ pip install -r requirements.txt
   ```
1. Start the consumer
   ```bash
   (venv) $ python3 test_consumer.py
   Waiting on messages...
   
   ```

### Start the Producer
1. Open a terminal to run the consumer
1. Navigate to `../memphis-setup-testing`.
1. Start the Python virtual environment created in the previous part
   ```bash
   $ source venv/bin/activate
   (venv) $
   ```
1. Start the producer
   ```bash
   (venv) $ python3 test_producer.py
   Sending message: This is a test message.
   Sending message: This is a test message.
   Sending message: This is a test message.
   Sending message: This is a test message.
   Sending message: This is a test message.   
   ```
1. Press Ctrl-C after a couple of seconds to kill the producer
1. Close the terminal

### Check the Consumer
In the terminal window running the consumer, you should see the following output:

```bash
Waiting on messages...
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')
message:  bytearray(b'This is a test message.')

```

### Check the Memphis.dev UI Station Details
Navigate to the Memphis.dev UI details screen for the "todo-cdc-events" station in your browser.  You should see the test messages, consumer, and producer:

![Memphis.dev UI station details screen with example messages](memphis_ui_station_with_test_messages.png)
