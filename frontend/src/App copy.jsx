// Semantic Space WebGL (React Three Fiber + FastAPI integration)

import { Canvas } from "@react-three/fiber"
import { OrbitControls } from "@react-three/drei"
import { useEffect, useState } from "react"
import { Vector3 } from "three"
import { create } from "zustand"

const useSemanticStore = create((set) => ({
  nodes: [],
  center: null,
  history: [],
  setCenter: async (sentence, pos) => {
    const newNodes = await generateNeighbors(sentence, pos)
    set((state) => ({
      center: sentence,
      history: [...state.history, sentence],
      nodes: newNodes
    }))
  }
}))

async function generateNeighbors(sentence, pos) {
  // Call FastAPI backend to expand ideas
  const res = await fetch("http://localhost:8000/expand", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sentence })
  })
  const data = await res.json()
  const ideas = data.ideas || []

  // Assign spatial positions
  const randomNearby = (base, range = 2) =>
    new Vector3(
      base.x + (Math.random() - 0.5) * range,
      base.y + (Math.random() - 0.5) * range,
      base.z + (Math.random() - 0.5) * range
    )

  // Optionally call /embed for center + ideas
  await fetch("http://localhost:8000/embed", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sentence })
  })

  for (const idea of ideas) {
    await fetch("http://localhost:8000/embed", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sentence: idea })
    })
  }

  return ideas.map((idea) => ({
    sentence: idea,
    position: randomNearby(pos)
  }))
}

function Node({ sentence, position }) {
  const setCenter = useSemanticStore((s) => s.setCenter)
  return (
    <mesh position={position} onClick={() => setCenter(sentence, position)}>
      <sphereGeometry args={[0.2, 16, 16]} />
      <meshStandardMaterial color="skyblue" />
    </mesh>
  )
}

function Labels() {
  const nodes = useSemanticStore((s) => s.nodes)
  return nodes.map((node, idx) => (
    <Node key={idx} sentence={node.sentence} position={node.position} />
  ))
}

export default function SemanticSpaceApp() {
  const setCenter = useSemanticStore((s) => s.setCenter)
  const center = useSemanticStore((s) => s.center)

  useEffect(() => {
    if (!center) {
      setCenter("The universe is expanding", new Vector3(0, 0, 0))
    }
  }, [center])

  return (
    <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />
      <Labels />
      <OrbitControls />
    </Canvas>
  )
}

