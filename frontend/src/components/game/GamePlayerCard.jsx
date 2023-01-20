const Cards = ({cards, isSelf}) => {
    if (!isSelf) {
        cards[0] = "back";
    }
    return (
        <>
            {cards.map(card => { return <img className="d-inline" src={"/images/" + card + ".jpg"} alt={card} width="120" height="180"></img>})}
        </>
    )
}

const GamePlayerCard = ({ name, bet, cards, isCurrent, isSelf }) => {
    
    return (
        <>
            <div className={isCurrent ? "border border-3 border-primary" : "border"}>
                <div>Name: {name}</div>
                <div>Bet: {bet}</div>
                <div>Cards: {cards && <Cards cards={cards} isSelf={isSelf} />}</div>
            </div>
        </>
    )
};

export default GamePlayerCard;