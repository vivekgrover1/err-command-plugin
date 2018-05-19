#!/usr/bin/python

from errbot import BotPlugin, botcmd , arg_botcmd
from fabric.api import *
from fabric.tasks import execute
import os

def cmd_exec(cmd):

        try:
          status = execute(local_exec, 'root',cmd)
          if  status.get('<local-only>')[1] == False :
           return status.get('<local-only>')[0], "green", "successfull"
          else:
           return status.get('<local-only>')[0], "danger", "executed"
        except :
           return "Coundn't Connect the host, please check the host name or try again.", "red", "failed"


def local_exec(user,cmd):
      """
        execute the ansible command on the local machine using fabric maodule and return the output
        of the command and status of the cmd execution success or failed.
      """

      env.user=user
      env.warn_only='True'
      result= local(cmd,capture=True)
      return result , result.failed


class COMMAND(BotPlugin):
    """
    Plugin to execute the command on remote machine.
    for ex .. execute command like ip, free, df, yum, etc.
    """

    @arg_botcmd('user_name', type=str)
    @arg_botcmd('hostname', type=str)
    def freememory(self, msg, hostname=None,user_name=None):
        """
        Command to get the free memory details.
        """

        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m raw --args='free -h' --private-key /root/errbot/ec2_key.pem -u {1} --become".format(hostname,user_name))
        count_success = value[0].count('| SUCCESS')
        count_failed = value[0].count('| FAILED')
        yield self.send_card(
                    title='command freememory is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action command freememory is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )

    @arg_botcmd('user_name', type=str)
    @arg_botcmd('hostname', type=str)
    def diskspace(self, msg, hostname=None,user_name=None):
        """
        Command to diskspace details with df.
        """

        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m raw --args='df -h' --private-key /root/errbot/ec2_key.pem -u {1} --become".format(hostname,user_name))
        count_success=value[0].count('| SUCCESS')
        count_failed=value[0].count('| FAILED')
        yield self.send_card(
                    title='command diskspace is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action diskspace is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )

    @arg_botcmd('user_name', type=str)
    @arg_botcmd('hostname', type=str)
    def ip(self, msg, hostname=None,user_name=None):
        """
        Command to ip details of the machine.
        """
        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m raw --args='ip a' --private-key /root/errbot/ec2_key.pem -u {1} --become".format(hostname,user_name))
        count_success=value[0].count('| SUCCESS')
        count_failed=value[0].count('| FAILED')
        yield self.send_card(
                    title='command ip is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action command ip is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )

    @arg_botcmd('user_name', type=str)
    @arg_botcmd('hostname', type=str)
    def nginx_stats(self, msg, hostname=None,user_name=None):
        """
        Command to get the nginx stats like to get the no of hits for status code.
        """
        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m raw --args='cut -d\" \" -f9 /var/log/nginx/access.log|sort |uniq -c |sort -k1,1nr 2>/dev/null|column -t' --private-key /root/errbot/ec2_key.pem -u {1} --become".format(hostname,user_name))
        count_success=value[0].count('| SUCCESS')
        count_failed=value[0].count('| FAILED')
        yield self.send_card(
                    title='nginx stats is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action nginx stats is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )


    @arg_botcmd('user_name', type=str)
    @arg_botcmd('package_name', type=str)
    @arg_botcmd('hostname', type=str)
    def yum_install(self, msg, hostname=None, package_name=None,user_name=None):
        """
        Command to install package through yum
        """
        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m yum --args='name={1} state=latest' --private-key /root/errbot/ec2_key.pem -u {2} --become".format(hostname,package_name,user_name))
        count_success=value[0].count('| SUCCESS')
        count_failed=value[0].count('| FAILED')
        yield self.send_card(
                    title='command yum is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action yum install is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )


    @arg_botcmd('user_name', type=str)
    @arg_botcmd('package_name', type=str)
    @arg_botcmd('hostname', type=str)
    def apt_install(self, msg, hostname=None, package_name=None,user_name=None):
        """
        Command to install the package though apt.
        """
        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m apt --args='name={1} state=latest' --private-key /root/errbot/ec2_key.pem -u {2} --become".format(hostname,package_name,user_name))
        count_success=value[0].count('| SUCCESS')
        count_failed=value[0].count('| FAILED')
        yield self.send_card(
                    title='command apt is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action apt install is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )



    @arg_botcmd('user_name', type=str)
    @arg_botcmd('service_name', type=str)
    @arg_botcmd('hostname', type=str)
    def service_status(self, msg, hostname=None, service_name=None,user_name=None):
        """
        Command to get the status of service.
        """

        yield  "Your task is now processing..."
        value = cmd_exec("ansible all -i '{0},' -m command --args='systemctl status {1}' --private-key /root/errbot/ec2_key.pem -u {2} --become".format(hostname,service_name,user_name))
        count_success = value[0].count('| SUCCESS')
        count_failed = value[0].count('| FAILED')
        yield self.send_card(
                    title='service status is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action service status is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )


    @arg_botcmd('user_name', type=str)
    @arg_botcmd('service_name', type=str)
    @arg_botcmd('hostname', type=str)
    def service_restart(self, msg, hostname=None, service_name=None,user_name=None):
        """
        Command to restart the service.
        """
        yield  "Your task is now processing..."
        value= cmd_exec("ansible all -i '{0},' -m service --args='name={1} state=restarted' --private-key /root/errbot/ec2_key.pem -u {2} --become".format(hostname,service_name,user_name))
        count_success=value[0].count('| SUCCESS ')
        count_failed=value[0].count('| FAILED')
        yield self.send_card(
                    title='service restart is executed',
                    in_reply_to=msg,
                    fields=(('Successfull',count_success), ('Failed',count_failed)),
                    body="Action service restart is  completed\nHost: {0}\nStatus: {1}\nResult:\n\n".format(hostname,value[2])+"```"+value[0]+"```",
                    color=value[1],
                )


