import React, { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Text } from '@react-three/drei'

const API = 'http://localhost:8000'

const fetchContinuum = async (sentence) => {
  const res = await fetch(`${API}/expand_continuum`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sentence }),
  })
  const data = await res.json()
  return data.nodes
}

const sphericalPosition = (i, total, radius = 2.5) => {
  const phi = Math.acos(1 - 2 * (i + 1) / total)
  const theta = Math.PI * (1 + Math.sqrt(5)) * (i + 1)
  return [
    radius * Math.cos(theta) * Math.sin(phi),
    radius * Math.sin(theta) * Math.sin(phi),
    radius * Math.cos(phi)
  ]
}

function IdeaNode({ position, label, onClick, isCenter }) {
  return (
    <group position={position}>
      <mesh onClick={onClick} scale={isCenter ? 1.5 : 1}>
        <sphereGeometry args={[0.2, 32, 32]} />
        <meshStandardMaterial color={isCenter ? 'orange' : 'skyblue'} />
      </mesh>
      <Text position={[0, 0.35, 0]} fontSize={0.15} color="white" maxWidth={2}>
        {label.slice(0, 36)}
      </Text>
    </group>
  )
}

export default function SemanticSpaceApp() {
  const [input, setInput] = useState("")
  const [center, setCenter] = useState(null)
  const [nodes, setNodes] = useState([])

  useEffect(() => {
    if (center) {
      fetchContinuum(center).then((results) => setNodes(results))
    }
  }, [center])

  return (
    <div style={{ width: '100vw', height: '100vh', overflow: 'hidden' }}>
      {!center && (
        <div style={{ position: 'absolute', zIndex: 1, top: 20, left: 20 }}>
          <input
            type="text"
            placeholder="Enter a sentence to start..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={{ padding: '10px', fontSize: '16px', width: '320px' }}
          />
          <button
            onClick={() => setCenter(input)}
            style={{ marginLeft: '10px', padding: '10px', fontSize: '16px' }}
          >
            Explore
          </button>
        </div>
      )}

      <Canvas camera={{ position: [0, 0, 6], fov: 55 }}>
        <ambientLight intensity={0.8} />
        <pointLight position={[10, 10, 10]} />
        <OrbitControls enableZoom enablePan enableRotate />

        {center && (
          <IdeaNode
            label={center}
            position={[0, 0, 0]}
            isCenter={true}
            onClick={() => {}}
          />
        )}

        {nodes.map((idea, i) => (
          <IdeaNode
            key={i}
            label={idea}
            position={sphericalPosition(i, nodes.length)}
            onClick={() => setCenter(idea)}
            isCenter={false}
          />
        ))}
      </Canvas>
    </div>
  )
}
