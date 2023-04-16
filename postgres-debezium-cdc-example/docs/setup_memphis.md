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
