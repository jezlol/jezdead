import pysnmp.hlapi as hlapi

def get_snmp(oid, target, community="public"):
    # Setting up the SNMP command with provided parameters
    iterator = hlapi.getCmd(
        hlapi.SnmpEngine(),
        hlapi.CommunityData(community),
        hlapi.UdpTransportTarget((target, 161)),
        hlapi.ContextData(),
        hlapi.ObjectType(hlapi.ObjectIdentity(oid))
    )

    # Executing SNMP command and retrieving the response
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    # Handling errors and displaying output
    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for varBind in varBinds:
            print(f"{varBind[0]} = {varBind[1]}")

# Set your router's IP address and OID for the specific interface
router_ip = "172.16.11.138"
interface_oid = "1.3.6.1.2.1.4.20.1.1.172.16.11.138"  # This is an example OID; replace it with the actual OID for your router's interface.

# Running the SNMP query
get_snmp(interface_oid, router_ip)
