import test from 'node:test'
import assert from 'node:assert/strict'
import { addSample, emptyWindow, forwardOrientation } from './visualSignals.js'

function face(noseX = 0.5) {
  const points = Array.from({ length: 264 }, () => ({ x: 0.5, y: 0.5 }))
  points[33] = { x: 0.4, y: 0.4 }
  points[263] = { x: 0.6, y: 0.4 }
  points[1] = { x: noseX, y: 0.47 }
  return points
}

test('orientation proxy and missing geometry', () => {
  assert.equal(forwardOrientation(face()), true)
  assert.equal(forwardOrientation(face(0.6)), false)
  assert.equal(forwardOrientation(null), null)
})

test('window counts stay nested and include missing samples', () => {
  const window = emptyWindow()
  addSample(window, face())
  addSample(window, face(0.6))
  addSample(window, null)
  addSample(window, null, false)
  assert.deepEqual([window.total_samples, window.valid_samples, window.face_samples, window.forward_samples], [4, 3, 2, 1])
  assert.equal('frame' in window, false)
})
