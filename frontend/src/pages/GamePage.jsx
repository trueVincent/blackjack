import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import GamePlayerCard from "../components/game/GamePlayerCard";
import * as game from "../game";

const GamePage = () => {
    const [players, setPlayers] = useState([]);
    const [dealer, setDelaer] = useState({});
    const [isCurrent, setIsCurrent] = useState(false);
    const nav = useNavigate();
    const name = sessionStorage.getItem("name");

    useEffect(() => {
        game.getGameDetail((dealer, players) => {
            setPlayers(players);
            setDelaer(dealer);
            setIsCurrent(isCurrentFn(name, dealer, players));
        });

        game.gameEnd(() => {
            return nav("/result");
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <>
            <div className="fs-1 fw-bold">Game</div>
            <div className={isCurrent ? "" : "d-none"}>Your turn</div>
            <div className="row">
                <div className="col-3">
                    <div className="fs-3">Dealer</div>
                    <GamePlayerCard name={dealer.name} bet={dealer.bet} cards={dealer.cards} isCurrent={dealer.is_current} isSelf={isSelf(name, dealer.name)} />
                    <div className="fs-3">Players</div>
                    {players.map(player => { return <GamePlayerCard name={player.name} bet={player.bet} cards={player.cards} isCurrent={player.is_current} isSelf={isSelf(name, player.name)} /> })}
                </div>
                <div className="col-6"></div>
                <div className="col-3">
                    <button className="btn btn-outline-secondary" type="button" disabled={isCurrent ? "" : "1"} onClick={handleHitBtnClickEvent}>Hit</button>
                    <button className="btn btn-outline-secondary" type="button" disabled={isCurrent && canDealerStand(name, dealer) ? "" : "1"} onClick={handleStandBtnClickEvent}>Stand</button>
                </div>
            </div>
        </>
    )
};

const isCurrentFn = (name, dealer, players) => {
    if (name === dealer.name && dealer.is_current) {return true};
    for (var i = 0; i < players.length; i++) {
        if (name === players[i].name && players[i].is_current) {return true};
    }
    return false;
}

const isSelf = (name, bet_name) => {
    return name === bet_name;
}

const canDealerStand = (name, dealer) => {
    if (name === dealer.name) {
        return dealer.cards_sum >= 17
    }
    return true;
}

const handleHitBtnClickEvent = () => {
    game.hit();
}

const handleStandBtnClickEvent = () => {
    game.stand();
}

export default GamePage;