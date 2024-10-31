from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd

def get_snmp(oid, target, community="public"):
    """
    Perform an SNMP GET request.

    Parameters:
    - oid: The OID to query.
    - target: The IP address of the SNMP agent (router).
    - community: SNMP community string (default is 'public').
    """
    # Create the iterator for the SNMP GET command
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((target, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    # Execute the command and handle the response
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    # Display results in terminal
    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for varBind in varBinds:
            print(f"{varBind[0].prettyPrint()} = {varBind[1].prettyPrint()}")

# Replace these values with the correct IP and OID
router_ip = "172.16.11.138"  # Replace with your router's IP address
# Example OID for IP address of interface e0/0; adjust based on your router's configuration.
interface_oid = "1.3.6.1.2.1.4.20.1.1"  # OID for IP addresses of interfaces

# Running the SNMP query
print(f"Performing SNMP GET on {router_ip} for OID: {interface_oid}")
get_snmp(interface_oid, router_ip)
