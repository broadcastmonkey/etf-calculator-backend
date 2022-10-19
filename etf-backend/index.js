require("dotenv").config();

const toBool = require("to-bool");
const httpServer = new (require("./sockets/http-server"))();
const chessServer = new (require("./sockets/socket-server"))(httpServer.server);

// chessServer.process.on("SIGINT", () => {
//     console.log("Caught interrupt signal... closing socket");
//     httpServer.close();
//     gamesManager.close();
//     users.save();

//     console.log("giving providers 20 sec to finish their jobs");

//     setTimeout(() => {
//         process.exit();
//     }, 1 * 1000);
// });
