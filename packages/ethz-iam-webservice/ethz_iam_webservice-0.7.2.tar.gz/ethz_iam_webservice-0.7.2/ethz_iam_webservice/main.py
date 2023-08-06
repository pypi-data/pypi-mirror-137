import datetime
import getpass
import json
import os
import re

import click
import yaml
from click.exceptions import ClickException

from ethz_iam_webservice.utils import to_date

from .ethz_iam import ETH_IAM_conn
from .utils import (
    check_password,
    format_leitzahl,
    format_notification,
    gen_password,
    to_date,
)
from .verbose import VERBOSE


class Service:
    def __init__(self, conn, data):
        self.conn = conn
        self.data = data
        if data:
            for key in data:
                setattr(self, key, data[key])


def _load_configuration(paths, filename=".ethz_iam_webservice"):
    if paths is None:
        paths = [os.path.expanduser("~")]

    # look in all config file paths
    # for configuration files and load them
    admin_accounts = []
    for path in paths:
        abs_filename = os.path.join(path, filename)
        if os.path.isfile(abs_filename):
            with open(abs_filename, "r") as stream:
                try:
                    config = yaml.safe_load(stream)
                    for admin_account in config["admin_accounts"]:
                        admin_accounts.append(admin_account)
                except yaml.YAMLError as e:

                    print(e)
                    return None

    return admin_accounts


def login(
    admin_username=None,
    admin_password=None,
    hostname="https://iam.passwort.ethz.ch",
    verify_certificates=True,
):
    hostname = hostname

    config_path = os.path.join(os.path.expanduser("~"), ".ethz_iam")
    if os.path.exists(config_path):
        import configparser

        raise Exception("not yet implemented")

    if admin_username is None:
        admin_username = os.environ.get(
            "IAM_USERNAME", input("Enter the admin username: ")
        )

    if admin_password is None:
        admin_password = os.environ.get(
            "IAM_PASSWORD",
            getpass.getpass(
                "Enter the password for admin user {}".format(admin_username)
            ),
        )

    return ETH_IAM_conn(
        admin_username,
        admin_password,
        hostname=hostname,
        verify_certificates=verify_certificates,
    )


def get_username_password(ctx):

    if ctx.obj["username"] is None:
        ctx.obj["username"] = os.environ.get("IAM_USERNAME", "") or click.prompt(
            text="Username",
            default=os.environ.get("USER", ""),
            show_default=True,
        )

    if ctx.obj["password"] is None:
        ctx.obj["password"] = os.environ.get("IAM_PASSWORD", "") or click.prompt(
            text="Password", hide_input=True
        )


@click.group()
@click.option(
    "-u",
    "--username",
    help="username of your ETHZ IAM admin account (if not provided, it will be prompted)",
)
@click.option(
    "--password",
    help="password of your ETHZ IAM admin account (if not provided, it will be prompted)",
)
@click.option(
    "-h", "--host", default="iam.passwort.ethz.ch", help="default: iam.passwort.ethz.ch"
)
@click.pass_context
def cli(ctx, host, username, password=None):
    """ETHZ IAM command-line tool."""
    ctx.ensure_object(dict)
    if not host.startswith("https://"):
        host = "https://" + str(host)
    ctx.obj["hostname"] = host
    ctx.obj["username"] = username
    ctx.obj["password"] = password


@cli.command("person", help="manage persons")
@click.argument("person")
@click.option(
    "-i",
    "--info",
    is_flag=True,
    default=True,
    help="all information about the person",
)
@click.pass_context
def person(ctx, person, info):
    get_username_password(ctx)

    e = login(ctx.obj["username"], ctx.obj["password"], ctx.obj["hostname"])
    person = e.get_person(person)

    print(json.dumps(person.data, indent=4, sort_keys=True))


@cli.command("group", help="manage security groups")
@click.argument("group")
@click.option("-d", "--delete", is_flag=True, help="delete this group")
@click.option(
    "-m",
    "--members",
    is_flag=True,
    help="show members of the group",
)
@click.option(
    "-i",
    "--info",
    is_flag=True,
    default=True,
    help="all information about the group",
)
@click.option(
    "-a",
    "--add",
    help="username to add to group. Can be used multiple times: -a us1 -a us2",
    multiple=True,
)
@click.option(
    "-r",
    "--remove",
    help="username to remove from group. Can be used multiple times: -r us1 -r us2",
    multiple=True,
)
@click.option(
    "-n",
    "--new",
    is_flag=True,
    help="create a new group",
)
@click.option(
    "--agroup",
    help="Admingroup for this group, required for new a group.",
)
@click.option(
    "-d",
    "--description",
    help="Description about this group.",
)
@click.option(
    "-t",
    "--target",
    help="Target system for this group. Can be used multiple times: -t AD -t LDAPS",
    multiple=True,
)
@click.pass_context
def group(
    ctx,
    group,
    delete,
    members,
    info,
    add=None,
    remove=None,
    new=None,
    agroup=None,
    description=None,
    target=None,
):
    """group modifications."""
    if add is None:
        add = ()
    if remove is None:
        remove = ()

    get_username_password(ctx)
    e = login(ctx.obj["username"], ctx.obj["password"], ctx.obj["hostname"])
    if new:
        if not agroup:
            raise click.ClickException("Please provide an admin group with --agroup")
        try:
            group = e.new_group(
                name=group, admingroup=agroup, description=description, targets=target
            )
        except ValueError as exc:
            raise ClickException(exc)
    else:
        try:
            group = e.get_group(group)
        except ValueError as exc:
            raise ClickException(exc)

    if add:
        group.add_members(*add)
    if remove:
        group.del_members(*remove)

    if add or remove or members:
        print(json.dumps(group.members))
        return

    if delete:
        click.confirm("Do you really want to delete this group?", abort=True)
        group.delete()
        return

    print(json.dumps(group.data, indent=4, sort_keys=True))


@cli.group("guest", help="manage guests")
@click.pass_context
def guest(ctx):
    get_username_password(ctx)
    iam = login(ctx.obj["username"], ctx.obj["password"], ctx.obj["hostname"])
    ctx.obj["iam"] = iam


@guest.command("get", help="get an existing guest")
@click.argument("username")
@click.pass_context
def get_guest(ctx, username):
    iam = ctx.obj["iam"]
    try:
        guest = iam.get_guest(username)
    except Exception as exc:
        raise click.ClickException(exc)
    print(json.dumps(guest._data_formatted(), indent=4, sort_keys=True))


@guest.command(
    "extend", help="extend validation of an existing guest. Default is today+1 year."
)
@click.option(
    "-e", "--endDate", help="specify end date of guest (YYYY-MM-DD or DD.MM.YYYY)."
)
@click.option(
    "-m", "--months", help="extend validation of an existing guest by this many months."
)
@click.argument("username")
@click.pass_context
def extend_guest(ctx, enddate, months, username):
    iam = ctx.obj["iam"]
    try:
        guest = iam.extend_guest(username, enddate, months)
        print(json.dumps(guest._data_formatted(), indent=4, sort_keys=True))
    except Exception as exc:
        raise click.ClickException(exc)


@click.option("-d", "--description", help="")
@click.option("-h", "--host", help="ETHZ Username of host")
@click.option(
    "-a",
    "--adminGroup",
    help="Name of the admin group this guest should be connected to. Default: same as the technical user which is creating this guest.",
)
@click.option(
    "-o",
    "--hostOrg",
    help="Leitzahl of host organization, see org.ethz.ch. Default: Leitzahl of the host.",
)
@click.option(
    "-c",
    "--technicalContact",
    help="email address of technical contact. Default: email of the host of this guest.",
)
@click.option(
    "-n",
    "--notification",
    help="g=guest, h=host, t=technical contact. Use any combination of the 3 chars. Defaults to «gh»",
)
@click.option(
    "-s", "--startDate", help="Start date of guest (YYYY-DD-MM). Default: today"
)
@click.option(
    "-e", "--endDate", help="End date of guest (YYYY-MM-DD). Default: today+1 year"
)
@guest.command("update", help="update an existing guest")
@click.argument("username")
@click.pass_context
def update_guest(
    ctx,
    description,
    hostorg,
    host,
    technicalcontact,
    admingroup,
    notification,
    startdate,
    enddate,
    username,
):

    if startdate:
        startdate = to_date(startdate)
    if enddate:
        enddate = to_date(enddate)

    iam = ctx.obj["iam"]
    try:
        guest = iam.update_guest(
            username=username,
            host=host,
            respAdminRole=admingroup,
            description=description,
            guestTechnicalContact=technicalcontact,
            notification=notification,
            hostOrg=hostorg,
            startDate=startdate,
            endDate=enddate,
        )
        print(json.dumps(guest._data_formatted(), indent=4, sort_keys=True))
    except Exception as exc:
        raise click.ClickException(exc)


@guest.command("new", help="create a new guest")
@click.option("-f", "--firstName", required=True, help="given name")
@click.option("-l", "--lastName", required=True, help="surname")
@click.option("-m", "--mail", required=True, help="email address")
@click.option("-d", "--description", required=True, help="")
@click.option("-h", "--host", required=True, help="ETHZ Username of host")
@click.option(
    "-a",
    "--adminGroup",
    required=True,
    help="Name of the admin group this guest should be connected to. Default: same as the technical user which is creating this guest.",
)
@click.option(
    "-b",
    "--dateOfBirth",
    help="birthdate in YYYY-MM-DD format. Default: Today's date + year 2000",
)
@click.option(
    "-o",
    "--hostOrg",
    help="Leitzahl of host organization, see org.ethz.ch. Default: Leitzahl of the host.",
)
@click.option(
    "-c",
    "--technicalContact",
    help="email address of technical contact. Default: email of the host of this guest.",
)
@click.option(
    "-n",
    "--notification",
    default="gh",
    help="g=guest, h=host, t=technical contact. Use any combination of the 3 chars. ",
)
@click.option(
    "-s", "--startDate", help="Start date of guest (YYYY-DD-MM). Default: today"
)
@click.option(
    "-e", "--endDate", help="End date of guest (YYYY-MM-DD). Default: today+1 year"
)
@click.option("--no-initpw", is_flag=True, help="do not change the initial password")
@click.pass_context
def new_guest(
    ctx,
    firstname,
    lastname,
    mail,
    description,
    dateofbirth,
    hostorg,
    host,
    technicalcontact,
    admingroup,
    notification,
    startdate,
    enddate,
    no_initpw,
):
    if dateofbirth:
        dateofbirth = to_date(dateofbirth)
    if startdate:
        startdate = to_date(startdate)
    if enddate:
        enddate = to_date(enddate)

    iam = ctx.obj["iam"]
    try:
        guest = iam.new_guest(
            firstName=firstname,
            lastName=lastname,
            mail=mail,
            host=host,
            respAdminRole=admingroup,
            description=description,
            guestTechnicalContact=technicalcontact,
            notification=notification,
            hostOrg=hostorg,
            startDate=startdate,
            endDate=enddate,
        )
        guest.save()
    except Exception as exc:
        raise click.ClickException(exc)

    ldap_password = gen_password()
    vpn_password = gen_password()
    guest_data = guest._data_formatted()
    guest_username = guest_data.get("username")

    if not guest_username:
        click.ClickException(
            "could not set inital password for the guest because the guest has no username."
        )

    if not no_initpw:
        guest_user = iam.get_user(guest_username)
        try:
            guest_user.set_password(password=ldap_password, service_name="LDAP")
            guest_data["init_ldap_password"] = ldap_password
        except Exception:
            pass

        try:
            guest_user.set_password(password=vpn_password, service_name="VPN")
            guest_data["init_vpn_password"] = vpn_password
        except Exception as exc:
            pass

    print(json.dumps(guest_data, indent=4, sort_keys=True))


@cli.command("user", help="manage users and their services")
@click.argument("username")
@click.option("-d", "--delete", is_flag=True, help="delete this user")
@click.option(
    "-i",
    "--info",
    is_flag=True,
    help="all information about the user",
)
@click.option(
    "-g",
    "--grant-service",
    multiple=True,
    help="grant a service to this user, e.g. AD, LDAPS, VPN. Use this option for every service you want to grant",
)
@click.option(
    "-r",
    "--revoke-service",
    multiple=True,
    help="revoke a service from this user, e.g. AD, LDAPS, VPN. Use this option for every service you want to revoke",
)
@click.option(
    "--init-password",
    is_flag=True,
    help="set the inital password(s) for this user (LDAPS and VPN). Returns the passwords in cleartext.",
)
@click.option(
    "--set-password",
    is_flag=True,
    help="set the password for that user. Use -s to specify for which service(s)",
)
@click.option(
    "-s",
    "--service",
    multiple=True,
    help="specify the service you want to set the password for",
)
@click.option(
    "-sp",
    "--service-password",
    help="set a password for the given service. Use the --service option to specify the service.",
)
@click.pass_context
def user(
    ctx,
    username,
    delete,
    info,
    grant_service=None,
    revoke_service=None,
    init_password=None,
    set_password=None,
    service_password=None,
    service=None,
):
    get_username_password(ctx)
    e = login(ctx.obj["username"], ctx.obj["password"], ctx.obj["hostname"])
    user = e.get_user(username)

    if delete:
        click.confirm("Do you really want to delete this user?", abort=True)
        user.delete()

    elif grant_service:
        for service_name in grant_service:
            user.grant_service(service_name)

    elif revoke_service:
        for service_name in revoke_service:
            user.revoke_service(service_name)
    elif init_password:
        ldap_password = gen_password()
        ad_password = gen_password()
        vpn_password = gen_password()
        init_pw = {}
        for service in user.data["services"]:
            if service.get("name") == "LDAP":
                try:
                    user.set_password(password=ldap_password, service_name="LDAP")
                    init_pw["init_ldap_password"] = ldap_password
                except Exception as exc:
                    pass
            elif service.get("name") in ["AD", "Active Directory", "Mailbox"]:
                try:
                    user.set_password(password=ad_password, service_name="AD")
                    init_pw["init_ad_password"] = ad_password
                except Exception as exc:
                    print(exc)
                    pass
            elif service.get("name") in ["WLAN_VPN"]:
                try:
                    user.set_password(password=vpn_password, service_name="VPN")
                    init_pw["init_vpn_password"] = vpn_password
                except Exception as exc:
                    pass
        print(json.dumps(init_pw, indent=4, sort_keys=True))

    elif service_password or set_password:
        if not service_password:
            service_password = click.prompt(text="Service Password", hide_input=True)
        if service:
            for s in service:
                try:
                    user.set_password(password=service_password, service_name=s)
                    print(f"successfully set password for service {s}")
                except ValueError as err:
                    print(err)
        elif "services" in user.data:
            for service in user.data["services"]:
                try:
                    user.set_password(
                        password=service_password, service_name=service["name"]
                    )
                    print(
                        "successfully set password for service {}".format(
                            service["name"]
                        )
                    )
                except ValueError as err:
                    print(err)
    else:
        print(json.dumps(user.data, indent=4, sort_keys=True))


if __name__ == "__main__":
    cli()
