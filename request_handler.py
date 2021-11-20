from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from users import create_user, login_user

class RareRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # def do_GET(self):
    #     print('***************')
    #     self._set_headers(200)
    #     self.wfile.write(json.dumps([]).encode())
    
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        raw_body = self.rfile.read(content_len)
        post_body = json.loads(raw_body)

        response = None
        
        if self.path == '/login':
            user = login_user(post_body)
            if user:
                response = {
                    'valid': True,
                    'token': user.id
                }
                self._set_headers(200)
            else:
                response = { 'valid': False }
                self._set_headers(404)

        if self.path == '/register':
            try:
                new_user = create_user(post_body)
                response = {
                    'valid': True,
                    'token': new_user.id
                }
            except Exception as e:
                response = {
                    'valid': False,
                    'error': str(e)
                }
            self._set_headers(201)

        self.wfile.write(json.dumps(response).encode())


def main():
    host = ''
    port = 8088
    print(f'listening on port {port}!')
    HTTPServer((host, port), RareRequestHandler).serve_forever()


    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2 items in it, 
        # which means the request was for`/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"

                else:
                    response = f"{get_all_users()}"
        
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

                # Is the resource `customers` and was there a
                # query parameter that specified the customer
                # email as a filtering value?
            if key == "email" and resource == "users":
                response = get_users_by_email(value)
            else:
                response = get_all_users()  
                #⭕️just to give it a fall back if the key or value has sth wrong
                # ??? will also need to give get_all_customers a default parameter: location_id = None

        self.wfile.write(response.encode())
        #⭕️⭕️⭕️ to fetch the response and use it in frontend: 
        # 示例: fetch("http://localhost:8000/posts").then(response => response.json()).then(setFeed)


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201) #Created
         
        content_len = int(self.headers.get('content-length', 0)) #⭕️headers are key-value pairs, like dictionary, but it's an object。⭕️
        post_body = self.rfile.read(content_len)  # raw post_body
        post_body = json.loads(post_body) # ⭕️Convert JSON string to a Python dictionary. (content was a string, cuz string is easy to send.)⭕️

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        new_user = None

        if resource == "users":
            new_user = create_user(post_body)
            # Encode the new animal and send in response
            self.wfile.write(f"{new_user}".encode())


# This function is not inside the class. It is the starting point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()
    # ⭕️ every time HTTPServer is called, it created a new instance to handle the new request.

if __name__ == "__main__":
    main()
