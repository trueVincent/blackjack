import RoomPlayerCard from "../components/game/RoomPlayerCard";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import * as game from "../game";

// Fix: 多次重複 render
// Fix: useEffect missing dependency

const WaitingRoomPage = () => {
    const [playerNames, setPlayerNames] = useState([]);
    const [dealerName, setDealerName] = useState("");
    const nav = useNavigate();

    useEffect(() => {
        game.getWaitingRoomDetails((dealerName, playerNames) => {
            setPlayerNames(playerNames);
            setDealerName(dealerName);
        });

        game.waitGameStart(() => {
            return nav("/game");
        });
    }, []);

    return (
        <>
            <div className="fs-1 fw-bold">WaitingRoom</div>
            <div className="row">
                <div className="col-3">
                    <div className="fs-3">Dealer</div>
                    <RoomPlayerCard name={dealerName} />
                    <div className="fs-3">Players</div>
                    {playerNames.map(name => { return <RoomPlayerCard name={name} /> })}
                </div>
                <div className="col-6"></div>
                <div className="col-3">
                    <button className="btn btn-outline-secondary" type="button" onClick={handleBeDealerClick}>Be dealer</button>
                    <button className="btn btn-outline-secondary" type="button" onClick={handleStartGameClick}>Start game</button>
                </div>
            </div>
        </>
    )
};

const handleBeDealerClick = () => {
    game.beDealer((res) => {
        if (!res) {
            alert("be dealer failed");
        }
    });
}

const handleStartGameClick = () => {
    game.startGame((arg) => {
        if (!arg) {
            alert("start game failed");
        }
    });
}

export default WaitingRoomPage;