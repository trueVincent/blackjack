const Cards = ({cards, isSelf}) => {
    let res = "";
    if (isSelf) {
        cards.map(card => {
            res += card + " ";
        })
    } else {
        res = "? ";
        for (let i = 1; i < cards.length; i++) {
            res += cards[i] + " ";
        }
    }
    return (<>{res}</>);
}

const GamePlayerCard = ({ name, bet, cards, isCurrent, isSelf }) => {
    
    return (
        <>
            <div className="border">
                <div>Name: {name}</div>
                <div>Bet: {bet}</div>
                <div>Cards: {cards && <Cards cards={cards} isSelf={isSelf} />}</div>
                {isCurrent && <div>Current</div>}
            </div>
        </>
    )
};

export default GamePlayerCard;