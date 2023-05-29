# Setting up Memphis
Memphis.dev must be configured for use with the CDC example.  In Memphis.dev, topics are called "stations".  When Memphis.dev is run for the first time, the web UI provides a wizard for creating your first station and user.

1. Point your browser to [http://localhost:9000](http://localhost:9000/).  Click "Sign in with root" at the bottom.
   ![Memphis.dev UI start page](memphis_ui_first_page.png)
1. Log in with the username "root" and the password "memphis"
   ![Memphis.dev UI root login](memphis_ui_login_root.png)
1. Create your first station.  Enter the station name as "raw-todo-cdc-events".  Leave the other settings at their defaults and click the "Next" button in the bottom right.
   ![Memphis.dev UI wizard create raw station page](memphis_ui_create_raw_station.png)
1. Create your first user.  Use the "todocdcservice" as the username and password.  Click the "Next" button in the bottom right.
   ![Memphis.dev UI wizard create user page](memphis_ui_create_user.png)
1. Click "Next" button on the producer and consumer example screens and finalize the creation.
1. You will be forwarded to the details screen for the new "raw-todo-cdc-events" station. Click the "arrow" button in upper left to go to the station overview page.
   ![Memphis.dev UI station details page](memphis_ui_raw_station_details.png)
1. On the station overview page, click the "Add New Station" button.
   ![Memphis.dev UI station overview page](memphis_ui_station_overview1.png)
1. Create a station named "cleaned-todo-cdc-events".
   ![Memphis.dev UI wizard create claned station page](memphis_ui_create_cleaned_station.png)
1. The station overview page will now show both stations.
   ![Memphis.dev UI station overview page](memphis_ui_station_overview2.png)
   
