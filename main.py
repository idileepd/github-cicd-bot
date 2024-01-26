from flask import Flask, Request, request
import subprocess

app = Flask(__name__)




@app.route('/webhook', methods=['GET'])
def webhook():
    webhookRun(request=request)


def webhookRun(request: Request):
    # Get the payload from the GitHub webhook
    # payload = request.data

    # Process the webhook payload (add your logic here)
    # For example, print the payload
    print('Received GitHub webhook payload:')
    # print(payload.decode('utf-8'))

    # Run some commands (add your commands here)
    try:
        x = subprocess.run(["ls"], check=True)
        print("0000",x)
        subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
        print('Git pull successful')
        # Add more commands as needed
        return 'Webhook received successfully', 200
    except subprocess.CalledProcessError as e:
        print(f'Error running command: {e}')

    return 'Webhook received successfully', 200


if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
