import React, { useEffect, useState } from "react";

type Market = {
  market_id: number;
  grade_id: number;
  date: string;
  price_fob_cif: number;
  usd_tnd_rate: number;
  source: string;
};

export default function Home() {
  const [health, setHealth] = useState<string>("checking…");
  const [market, setMarket] = useState<Market[]>([]);

  useEffect(() => {
    fetch(process.env.NEXT_PUBLIC_API_URL + "/health")
      .then(r => r.json()).then(d => setHealth(d.status))
      .catch(() => setHealth("offline"));
    fetch(process.env.NEXT_PUBLIC_API_URL + "/market_data")
      .then(r => r.json()).then(setMarket).catch(()=>{});
  }, []);

  return (
    <main style={{padding: 24, fontFamily: 'sans-serif'}}>
      <h1>Oiltracker</h1>
      <p>API status: {health}</p>
      <h2>Derniers prix marché</h2>
      <table>
        <thead><tr><th>ID</th><th>Grade</th><th>Date</th><th>Prix</th><th>USD/TND</th><th>Source</th></tr></thead>
        <tbody>
          {market.map(m => (
            <tr key={m.market_id}><td>{m.market_id}</td><td>{m.grade_id}</td><td>{m.date}</td><td>{m.price_fob_cif}</td><td>{m.usd_tnd_rate}</td><td>{m.source}</td></tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
