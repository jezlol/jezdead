from pysnmp.hlapi import SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity, getCmd, setCmd, OctetString

# ตั้งค่าข้อมูลพื้นฐาน
router_ip = '172.16.11.138'  # IP ของเราเตอร์
community = 'public'          # ชื่อชุมชน
sys_contact_email = 'thanpaarnjez@email.kmutnb.ac.th'  # เปลี่ยนเป็นอีเมลของนักศึกษา
student_name = 'Thanormsak Sudsee'  # เปลี่ยนชื่อของนักศึกษา

# OID ที่ใช้ในการดึงข้อมูล
sys_descr_oid = '1.3.6.1.2.1.1.1.0'  # sysDescr
sys_uptime_oid = '1.3.6.1.2.1.1.3.0'  # sysUpTime
sys_contact_oid = '1.3.6.1.2.1.1.4.0'  # sysContact
sys_name_oid = '1.3.6.1.2.1.1.5.0'  # sysName

def get_snmp(oid):
    """
    ทำการดึงข้อมูล SNMP
    """
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((router_ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        for varBind in varBinds:
            return varBind[1]  # คืนค่าข้อมูล

def set_snmp(oid, value):
    """
    ทำการแก้ไขข้อมูล SNMP
    """
    iterator = setCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((router_ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid), value)
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"Error: {errorIndication}")
    elif errorStatus:
        print(f"Error: {errorStatus.prettyPrint()} at {errorIndex}")
    else:
        print(f"Successfully set {oid} to {value}")

# แสดงข้อมูลระบบ
print("Fetching system information...")
sys_descr = get_snmp(sys_descr_oid)
sys_uptime = get_snmp(sys_uptime_oid)

print(f"System Description: {sys_descr}")
print(f"System Uptime: {sys_uptime}")

# ตั้งค่าข้อมูลใหม่
print("\nUpdating system information...")
set_snmp(sys_contact_oid, OctetString(sys_contact_email))  # เปลี่ยนชื่อผู้ติดต่อ
set_snmp(sys_name_oid, OctetString(student_name))  # เปลี่ยนชื่อเครื่อง

print("\nSystem information updated successfully.")
