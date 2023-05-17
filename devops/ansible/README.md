# How to automate deployment using Ansible

> **Note**: Values in angle brackets are example values e.g. IP: `<18.185.84.203>`

## Create deployment server

You can create EC2 instance on AWS. In case of AWC EC2 You probably have:
- [x] instance address: `<ubuntu@18.185.84.203>`
- [x] private key for SSH connection: `<server_priv_rsa_key>`<br>

> **Note**: Public pair for `<server_priv_rsa_key>` private key is added to the server's `~/.ssh/authorized_keys`<br>
> already, which makes it possible to connect via ssh.

> **Note**: Make sure ssh and http(s) traffic is enabled to deployment server.<br>
> Rules with source `0.0.0.0/0` allow all IP addresses to access your instance.

## Prepare dedicated RSA key for Ansible deployment to be able to connect to deployment server via SSH

Create RSA key pair:
```bash
ssh-keygen -t rsa -P "" -f ./deployment-rsa
```
Above command will create two files:
1. `./deployment-rsa`: private RSA key. *It needs to stay secret*. Upload this key where it will be available<br>
for deployment process e.g. add it to GitHub secrets in order to use it during automated GitHub workflow.<br>
The purpose of having that private key is to authorize during ssh connection between deployment process and actual<br>
deployment server.
2. `./deployment-rsa.pub`: public RSA key. It's no secret. Server that keeps it's content in `~/.ssh/authorized_keys`,<br>
allows anyone that has its private companion `./deployment-rsa` to connect via ssh.

Send `./deployment-rsa.pub` public RSA key to deployment server:
```bash
chmod 400 ./server_priv_rsa_key
scp -i "./server_priv_rsa_key" -o StrictHostKeyChecking=no ./deployment-rsa.pub ubuntu@18.185.84.203:/home/ubuntu
```

Connect to deployment server:
```bash
ssh -i "./server_priv_rsa_key" -o StrictHostKeyChecking=no ubuntu@18.185.84.203
```

Add `<deployment-rsa.pub>` public RSA key to deployment server's `~/.ssh/authorized_keys`.<br>
This step will make SSH connection possible using corresponding `<deployment-rsa>` RSA private key.
```bash
sudo mv /home/ubuntu/deployment-rsa.pub ~/.ssh/
cat ~/.ssh/deployment-rsa.pub >> ~/.ssh/authorized_keys
```

It should be possible to connect to deployment server using recently created deployment RSA key from your local server:
```bash
chmod 400 ./deployment-rsa && \
ssh -i "./deployment-rsa" -o StrictHostKeyChecking=no ubuntu@18.185.84.203
```

So far You have prepared deployment server, and You made SSH connection possible with dedicated RSA private key `<deployment-rsa`.<br>
You now have:
- [x] Deployment server: `<ubuntu@18.185.84.203>`
- [x] Deployment dedicated private key: `<deployment-rsa>`

Now it's time to prepare Ansible scripts that using above is able to make automated deployment on deployment server.

## Prepare Ansible scripts to make automated deployment on deployment server

Usually CI/CD actions are Docker based so in order to test following deployment steps,<br>
I recommend to use Ubuntu Docker container.<br>
In GitHub actions I'll make use of repository secrets to pass RSA private key, so to be consistent I'll create ENV variable.
```bash
docker run \
  --rm -it \
  --name ubuntu-tmp \
  -e PRIVATE_RSA_KEY=$(base64 -i ./deployment-rsa) \
  -v  $(pwd):/website-project \
  ubuntu:latest bash
```

Enable SSH connection
```bash
# Make sure ~/.ssh/ exists
mkdir -p ~/.ssh

# Inject RSA private key (~/.ssh/id_rsa is default for SSH)
echo $PRIVATE_RSA_KEY | base64 --decode > ~/.ssh/id_rsa && \
chmod 400 ~/.ssh/id_rsa

# Install SSH
apt-get update && \
apt-get upgrade -y && \
apt-get install openssh-client -y

# You should no be able to connect (still with StrictHostKeyChecking=no flag)
# ssh -o StrictHostKeyChecking=no ubuntu@18.185.84.203

# Add deployment server to known_hosts file - will prevent fingerprint prompt
if ! test -e ~/.ssh/authorized_keys; then \
  echo "Creating path: ~/.ssh/authorized_keys"; \
  touch ~/.ssh/authorized_keys; \
else \
  echo "Path already exists: ~/.ssh/authorized_keys"; \
fi && \
ssh-keyscan 18.185.84.203 >> ~/.ssh/known_hosts

# SSH connection setup is done
# ssh ubuntu@18.185.84.203
```

Get ready for Ansible part.<br>
Install Ansible
```bash
apt update && \
# Turns off Ansible installation prompts
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \
apt install ansible -y && \
ansible --version
```

Install extra Ansible plugins
```bash
ansible-galaxy --version
ansible-galaxy collection install community.docker
```

Run `hello-world.yaml` playbook on `<ubuntu@18.185.84.203>` deployment server
```bash
ansible-playbook -i "ubuntu@18.185.84.203," ./website-project/devops/ansible/playbooks/hello-world.yaml
```
