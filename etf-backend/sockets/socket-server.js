const socketIO = require("socket.io"); // sock
const toBool = require("to-bool");
const { spawn } = require("child_process");
class ChessSocketServer {
  users = [];

  getUserBySocketId = (socketId) => {
    return this.users.find((user) => user.id === socketId);
  };
  addUser = ({ id }) => {
    const existingUser = this.users.find((user) => user.id === id);
    if (existingUser) {
      console.log("user already exists...");
      console.log(existingUser);
      return { error: `socket ${id} is already connected` };
    }
    const user = { id, lastPing: 0 };
    this.users.push(user);
    return { user };
  };
  usersCount = () => this.users.length;
  removeUser = (id) => {
    const userIndex = this.users.findIndex((user) => user.id === id);
    if (userIndex !== -1) {
      return this.users.splice(userIndex, 1)[0];
    }
  };

  constructor(server) {
    this.io = socketIO(server, {
      cors: {
        origin: "*",
        methods: ["GET", "POST"],
        allowedHeaders: [
          "my-custom-header",
          "origin",
          "x-requested-with",
          "content-type",
        ],
        credentials: true,
      },
    });

    this.io.on("connection", (socket) => {
      try {
        console.log("[n]   new client...");
        socket.on("join", (param, callback) => {
          this.handleJoin(socket, param, callback);
        });

        socket.on("newScoreRequest", (data, callback) => {
          this.handleNewScoreRequest(socket, data, callback);
        });

        socket.on("disconnect", () => {
          this.handleDisconnect(socket);
        });
      } catch {
        console.log("err :(");
      }
    });
  }

  handleJoin = async (socket, param, callback) => {
    const isLogged = this.getUserBySocketId(socket.id);
    if (isLogged) {
      console.log(
        "handleJoin",
        "user withc socket id: " + socket.id + " already exists..."
      );
    }

    console.log("adding user : ", socket.id);

    const { error, user } = this.addUser({ id: socket.id });

    if (error) return callback ? callback({ error: "error 2" }) : null;

    console.log("user added", user);
    //socket.join("chess");
    //if (callback) callback("chess"); // obj: successfuly joined ?
  };

  handleDisconnect = (socket) => {
    // console.log("disconnected socket... trying to remove user fom Users Array");
    const user = this.removeUser(socket.id);
    if (user) {
      // console.log("login of disconnected user", user.id);
    } else {
      // console.log("disconnected socket was not registered in Users Array");
    }
  };
  // ---------
  //----------
  handleNewScoreRequest = async (socket, data, callback) => {
    if (callback) callback({ msg: "new_game_request" });
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn("python", [
      "./etf-backend/calculate-etf.py",
      data.score,
      data.portfolio,
    ]);

    if (data.portfolio > 1000000) return;
    // collect data from script

    console.log("score: " + data.score + ",  portfolio: " + data.portfolio);
    dataToSend = "";

    python.stdout.on("data", function (data) {
      dataToSend += data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on("close", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      console.log(JSON.parse(dataToSend));
      socket.emit("scoreRequestFinished", JSON.parse(dataToSend));
      // send data to browser
      //res.send(dataToSend);
    });
    //socket.emit("scoreRequestFinished", "your score is : " + data.score);
  };

  debugLog = (functionName, data) => {
    if (toBool(process.env.LOG_ENABLED_SOCKETS_FUNCTION_HEADER))
      console.log(
        `>>>> Sockets::${functionName} ` + JSON.stringify(data, null, 4)
      );
  };
}

module.exports = ChessSocketServer;
