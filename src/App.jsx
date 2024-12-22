import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
    const [wrestlers, setWrestlers] = useState([]);// Stores list of all wrestlers
    const [wrestler1, setWrestler1] = useState('');// Stores selected wrestler 1's name
    const [wrestler2, setWrestler2] = useState('');// Stores selected wrestler 2's name
    const [result, setResult] = useState(null);    // Stores match result

    useEffect(() => {
          // Makes GET request to http://localhost:5000/api/wrestlers
        axios.get('http://localhost:5000/api/wrestlers')
            .then(response => setWrestlers(response.data))// Stores wrestlers in state
            .catch(error => console.error('Error fetching wrestlers:', error));
    }, []);

    const simulateMatch = () => {
        if (wrestler1 && wrestler2 && wrestler1 !== wrestler2) {
            // Find the array indexes of selected wrestlers
            const wrestler1Id = wrestlers.findIndex(wrestler => wrestler.name === wrestler1);
            const wrestler2Id = wrestlers.findIndex(wrestler => wrestler.name === wrestler2);

            axios.post('http://localhost:5000/api/simulate', {
                wrestler1: wrestler1Id, //Pass wrestler and index in array
                wrestler2: wrestler2Id
            })
            .then(response => {
                setResult(response.data); //Get winner
            })
            .catch(error => console.error('Error simulating match:', error));
        } else {
            alert('Please select two different wrestlers.');
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>WWE Fantasy Match Simulator</h1>

            <div>
                <label>Wrestler: </label>
                <select value={wrestler1} onChange={(e) => setWrestler1(e.target.value)}>
                    <option value="">Select Wrestler 1</option>
                    {wrestlers.map((wrestler, idx) => (
                        <option key={idx} value={wrestler.name}>
                            {wrestler.name}
                        </option>
                    ))}
                </select>
            </div>

            <div style={{ marginTop: '10px' }}>
                <label>Wrestler\: </label>
                <select value={wrestler2} onChange={(e) => setWrestler2(e.target.value)}>
                    <option value="">Select Wrestler 2</option>
                    {wrestlers.map((wrestler, idx) => (
                        <option key={idx} value={wrestler.name}>
                            {wrestler.name}
                        </option>
                    ))}
                </select>
            </div>

            <button onClick={simulateMatch} style={{ marginTop: '20px' }}>
                Simulate Match
            </button>

            {result && (
                <div style={{ marginTop: '20px' }}>
                    <h2>Match Result</h2>
                    <p>Winner: {result.winner.name} with the {result.winner.special_move}!</p>
                </div>
            )}
        </div>
    );
};

export default App;