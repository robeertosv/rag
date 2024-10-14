const express = require('express')
const app = express();
const server = require('http').createServer(app)
const socketIo = require('socket.io')
const amqp = require('amqplib/callback_api.js')
const path = require('path')

const PORT = 80;
const io = socketIo(server)

app.use(express.json())
app.use(express.static(path.join(__dirname, 'pages')))

function reemplazarComillas(texto) {
    return texto.replace(/'/g, '"');
}

app.get('/', (req, res) => {
    return res.status(200).sendFile(path.join(__dirname, 'pages/index.html'))
})

app.post('/api/prompt', (req, res) => {
    let { message } = req.body;
    console.log(message)
    res.send(message)

    //amqp.connect(`amqp://${user}:${pass}@${host}:${mqport}`, (err, conn) => {
    amqp.connect(`amqp://localhost`, (err, conn) => {
        conn.createChannel((err, ch) => {
            let q = 'message';
            ch.assertQueue(q, { durable: false });
            ch.sendToQueue(q, Buffer.from(message));
        })
    })
})

amqp.connect(`amqp://localhost`, (err, conn) => {
    if (err) { throw err; }
    conn.createChannel((err, ch) => {
        let q = 'result';
        ch.assertQueue(q, { durable: false });
        ch.consume(q, (msg) => {
            console.log(JSON.parse(msg.content.toString()))
            io.emit('result', JSON.parse(msg.content.toString()));

        }, { noAck: true })
    })
})

io.on('connection', (socket) => {
    console.log('Nuevo cliente conectado');

    // Manejar la desconexión del cliente
    socket.on('disconnect', () => {
        console.log('Cliente desconectado');
    });
});

server.listen(PORT, () => {
    console.log('http://localhost')
})