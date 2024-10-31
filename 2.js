const express = require('express');
const { Session } = require('snmp-native');
const snmp = require('net-snmp');

const app = express();
const port = 3000;
const ip_add = '192.168.75.52';
const community = 'private';

const managePort = (port, action, callback) => {
  const session = new Session({ host: ip_add, community });
  const oid = [1, 3, 6, 1, 2, 1, 2, 2, 1, 7, port];
  session.set({ oid, value: action, type: 2 }, (error) => {
    callback(error ? error : null);
    session.close();
  });
};

const getPortData = (oid, callback) => {
  const session = new Session({ host: ip_add, community });
  session.getSubtree({ oid }, (error, varbinds) => {
    const data = {};
    if (!error) varbinds.forEach(vb => data[vb.oid[vb.oid.length - 1]] = vb.value);
    callback(error, data);
    session.close();
  });
};

const getPortName = (callback) => getPortData([1, 3, 6, 1, 2, 1, 2, 2, 1, 2], callback);
const getPortStatus = (callback) => getPortData([1, 3, 6, 1, 2, 1, 2, 2, 1, 7], (error, data) => {
  const portStatus = {};
  if (!error) Object.entries(data).forEach(([port, value]) => portStatus[port] = value === 1 ? 'Up' : 'Down');
  callback(error, portStatus);
});

const resStatus = (res, error, status = 200) => res.status(status).send(error ? `Error: ${error.message}` : '');

const resHTML = (res, portStatus, portName) => res.send(`
  <html>
    <head>
      <title>Custom SNMP Port Status</title>
      <style>.status-up { color: green; } .status-down { color: red; }</style>
    </head>
    <body>
      <h1>Custom SNMP Port Status</h1>
      <table><thead><tr><th>Port Name</th><th>Actions</th></tr></thead>
        <tbody>
          ${Object.entries(portStatus).filter(([port]) => port !== 'Null0').map(([port]) => `
            <tr><td class="${portStatus[port] === 'Up' ? 'status-up' : 'status-down'}">
              ${portName[port] || 'Port ' + port}</td>
              <td><a href="/manage/${port}/1">เปิด</a> <a href="/manage/${port}/2">ปิด</a></td></tr>`).join('')}
        </tbody>
      </table>
      <form action="/snmp-data" method="get"><button type="submit">View SNMP Data</button></form>
    </body>
  </html>`);

app.get('/manage/:port/:action', (req, res) => {
  const { port, action } = req.params;
  managePort(port, action, (error) => res.redirect(error ? '/error' : '/'));
});

app.get('/error', (req, res) => resStatus(res, 'Error occurred', 500));

app.get('/', (req, res) => {
  getPortStatus((error, portStatus) => {
    if (error) return resStatus(res, error, 500);
    getPortName((nameError, portName) => {
      if (nameError) return resStatus(res, nameError, 500);
      resHTML(res, portStatus, portName);
    });
  });
});

app.get('/snmp-data', (req, res) => {
  const TimeUp = '.1.3.6.1.2.1.31.1.1.1.2.4';
  const session = snmp.createSession(ip_add, community);

  const oids = [TimeUp];
  session.get(oids, (error, varbinds) => {
    if (error) return res.status(500).send(`Error retrieving SNMP data: ${error}`);
    const snmpData = varbinds.map((vb) => `${vb.oid} = ${vb.value}`).join('<br>');
    res.send(`
      <html>
        <head><title>SNMP Data</title></head>
        <body><h1>SNMP Data</h1><p>${snmpData}</p>
          <form action="/" method="get"><button type="submit">SET port Switch or Router</button></form>
        </body>
      </html>`);
    session.close();
  });
});


app.listen(port, () => console.log(`Server is running on http://localhost:${port}`));