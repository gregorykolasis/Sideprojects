from fabric import Connection as connection, task



#result = Connection( host = '78.159.98.230' , port = 8822 ,  user='root' , ).run('uname -s')
#msg = f"Ran {result.command} on {result.connection.host}, got stdout:\n{result.stdout}"
#print(msg.format(result))


# with Connection(
#     host = '188.118.27.230',
#     port = 8822,
#     user = "ag3ntf4ctory",
#     connect_kwargs={"password": "1nt3ll1tz3nt!@#"}
# ) as c:
#     with c.cd("/home"):
#         c.run("ls")

def deploy():
    with connection(
    host = '188.118.27.230',
    port = 8822,
    user = "ag3ntf4ctory",
    connect_kwargs={"password": "1nt3ll1tz3nt!@#"}
    ) as c:
        try:
            c.run('mkdir /home/ag3ntf4ctory/testdic')
            c.run('mkdir /home/ag3ntf4ctory/testdic2')
            c.run('mkdir /home/ag3ntf4ctory/testdic3')
            c.run('mkdir /home/ag3ntf4ctory/testdic4')
        except Exception as e:
            print(e)
        c.put('./lol.txt', '/home/ag3ntf4ctory')

deploy()



