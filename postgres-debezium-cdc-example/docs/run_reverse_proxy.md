# Running the Reverse Proxy

## Start the Reverse Proxy
1. Open a terminal to run the consumer
1. Navigate to `../reverse-proxy`.
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
1. Start the reverse proxy
   ```bash
   (venv) $ MEMPHIS_HOST=localhost MEMPHIS_USERNAME=todocdcservice MEMPHIS_PASSWORD=todocdcservice python3 reverse_proxy.py
    * Serving Flask app 'reverse_proxy'
    * Debug mode: on
    INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:8000
    * Running on http://192.168.1.128:8000
    INFO:werkzeug:Press CTRL+C to quit
    INFO:werkzeug: * Restarting with stat
    WARNING:werkzeug: * Debugger is active!
    INFO:werkzeug: * Debugger PIN: 127-986-130
   ```
