const snmp = require('net-snmp');

// Configuration for the SNMP agent (router)
const routerIp = '172.16.11.138'; // Replace with your router's IP address
const community = 'public'; // Replace with your community string
const oid = '1.3.6.1.2.1.4.20.1.1'; // OID for IP addresses of interfaces

// Create an SNMP session
const session = snmp.createSession(routerIp, community);

// Perform the SNMP GET operation
session.get([oid], (error, varbinds) => {
    if (error) {
        console.error(`Error: ${error}`);
    } else {
        varbinds.forEach((varbind) => {
            if (snmp.isVarbindError(varbind)) {
                console.error(`Error: ${snmp.varbindError(varbind)}`);
            } else {
                console.log(`${varbind.oid} = ${varbind.value}`);
            }
        });
    }

    // Close the session
    session.close();
});
