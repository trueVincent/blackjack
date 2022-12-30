import { io } from "socket.io-client";

const socket = io("http://35.209.67.28/");

let loginCb = () => {};
const login = (name, cb) => {
    loginCb = cb;
    socket.emit("get_player", name);
}
socket.on("get_player_result", (arg) => {
    if (arg.success) {
        loginCb();
    } else {
        alert("Login failed");
    }
});

let registerCb = () => {};
const register = (name, cb) => {
    registerCb = cb;
    socket.emit("create_player", name);
    
}
socket.on("create_player_result", (arg) => {
    if (arg.success) {
        registerCb();
    } else {
        alert("register failed");
    }
})

let joinCb = () => {};
const join = (cb) => {
    joinCb = cb;
    socket.emit("join_game");
}
socket.on("join_game_result", () => {
    joinCb();
})

let logoutCb = () => {};
const logout = (cb) => {
    logoutCb = cb;
    socket.emit("logout");
    
}
socket.on("logout_result", () => {
    logoutCb();
})

let getWaitingRoomDetailsCb = () => {};
const getWaitingRoomDetails = (cb) => {
    getWaitingRoomDetailsCb = cb;
    socket.emit("get_waiting_room_details");
}
socket.on("get_waiting_room_details", (arg) => {
    getWaitingRoomDetailsCb(arg.dealer_name, arg.player_names);
})

let beDealerCb = () => {};
const beDealer = (cb) => {
    beDealerCb = cb;
    socket.emit("be_dealer");
}
socket.on("be_dealer_result", (arg) => {
    beDealerCb(arg);
})

let startGameCb = () => {};
const startGame = (cb) => {
    startGameCb = cb;
    socket.emit("start_game");
}
socket.on("start_game_result", (arg) => {
    startGameCb(arg);
})

let waitGameStartCb = () => {};
const waitGameStart = (cb) => {
    waitGameStartCb = cb;
}
socket.on("wait_game_start", () => {
    waitGameStartCb();
})

let getGameDetailCb = () => {};
const getGameDetail = (cb) => {
    getGameDetailCb = cb;
    socket.emit("get_game_detail");
}
socket.on("get_game_detail", (arg) => {
    getGameDetailCb(arg.dealer, arg.players);
})

const hit = () => {
    socket.emit("hit");
}

const stand = () => {
    socket.emit("stand");
}

let gameEndCb = () => {};
const gameEnd = (cb) => {
    gameEndCb = cb;
}
socket.on("game_end", () => {
    gameEndCb();
})

let getGameResultCb = () => {};
const getGameResult = (cb) => {
    getGameResultCb = cb;
    socket.emit("get_result");
}
socket.on("get_result", (arg) => {
    getGameResultCb(arg.dealer, arg.players);
})


export { login, register, join, logout, getWaitingRoomDetails, beDealer, startGame, waitGameStart, getGameDetail, hit, stand, gameEnd, getGameResult }