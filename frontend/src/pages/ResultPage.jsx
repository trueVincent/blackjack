import ResultPlayerCard from "../components/game/ResultPlayerCard";
import { useNavigate } from "react-router-dom";
import * as game from "../game";
import { useState, useEffect } from "react";

const ResultPage = () => {
    const [dealer, setDealer] = useState({});
    const [players, setPlayers] = useState([]);
    const nav = useNavigate();

    useEffect(() => {
        game.getGameResult((dealer, players) => {
            setDealer(dealer);
            setPlayers(players);
        })
    }, [])

    return (
        <>
            <div className="fs-1 fw-bold">Result</div>
            <div className="row">
                <div className="col-9">
                    <div className="fs-3">Dealer</div>
                    <ResultPlayerCard name={dealer.name} bet={dealer.bet} balance={dealer.balance} cards={dealer.cards} />
                    <div className="fs-3">Players</div>
                    {players.map(player => { return <ResultPlayerCard name={player.name} bet={player.bet} balance={player.balance} cards={player.cards} /> })}
                </div>
                <div className="col-3">
                    <button className="btn btn-outline-secondary" type="button" onClick={() => handleAgainBtnClickEvent(nav)}>Again</button>
                    <button className="btn btn-outline-secondary" type="button" onClick={() => handleLeaveBtnClickEvent(nav)}>Leave</button>
                </div>
            </div>
        </>
    )
};

const handleAgainBtnClickEvent = (nav) => {
    game.join(() => {
        return nav("/waitingroom");
    })
};

const handleLeaveBtnClickEvent = (nav) => {
    return nav("/");
};

export default ResultPage;