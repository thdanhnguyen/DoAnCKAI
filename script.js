let cities = ["Hà Nội", "Hải Phòng", "Đà Nẵng", "Huế", "TP.HCM", "Cần Thơ", "Nha Trang", "Đà Lạt"]
let cityCoords = {
  "Hà Nội": [105.8, 21.0],
  "Hải Phòng": [106.7, 20.8],
  "Đà Nẵng": [108.2, 16.0],
  Huế: [107.6, 16.5],
  "TP.HCM": [106.7, 10.8],
  "Cần Thơ": [105.8, 10.0],
  "Nha Trang": [109.2, 12.2],
  "Đà Lạt": [108.4, 11.9],
}

let results = {}
let currentTab = "default"

function switchTab(tabName) {
  currentTab = tabName

  // Update tab buttons
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("active"))
  event.target.classList.add("active")

  // Update tab content
  document.querySelectorAll(".tab-content").forEach((content) => content.classList.remove("active"))
  document.getElementById(`tab-${tabName}`).classList.add("active")

  // Update cities list/editor
  if (tabName === "default") {
    updateCitiesList()
  } else if (tabName === "manual") {
    updateCitiesEditor()
  }
}

function updateCitiesList() {
  const citiesList = document.getElementById("citiesList")
  citiesList.innerHTML = cities
    .map((city, i) => `<div class="city-item">${i + 1}. ${city} (${cityCoords[city][0]}, ${cityCoords[city][1]})</div>`)
    .join("")
}

function updateCitiesEditor() {
  const editor = document.getElementById("citiesEditor")
  editor.innerHTML = cities
    .map(
      (city, i) => `
        <div class="city-input-row">
            <input type="text" value="${city}" placeholder="Tên thành phố" onchange="updateCity(${i}, 'name', this.value)">
            <input type="number" step="0.1" value="${cityCoords[city][0]}" placeholder="Kinh độ" onchange="updateCity(${i}, 'lon', this.value)">
            <input type="number" step="0.1" value="${cityCoords[city][1]}" placeholder="Vĩ độ" onchange="updateCity(${i}, 'lat', this.value)">
            <button class="btn-small btn-remove" onclick="removeCity(${i})">🗑️</button>
        </div>
    `,
    )
    .join("")
}

function updateCity(index, field, value) {
  const oldName = cities[index]

  if (field === "name") {
    const newName = value.trim()
    if (newName && newName !== oldName) {
      cities[index] = newName
      cityCoords[newName] = cityCoords[oldName]
      delete cityCoords[oldName]
    }
  } else if (field === "lon") {
    cityCoords[oldName][0] = Number.parseFloat(value)
  } else if (field === "lat") {
    cityCoords[oldName][1] = Number.parseFloat(value)
  }

  drawCities()
}

function addCityRow() {
  const newCity = `Thành phố ${cities.length + 1}`
  cities.push(newCity)
  cityCoords[newCity] = [106.0, 16.0] // Default coordinates
  updateCitiesEditor()
  drawCities()
}

function removeCity(index) {
  if (cities.length <= 3) {
    alert("Cần ít nhất 3 thành phố để giải bài toán TSP!")
    return
  }

  const cityName = cities[index]
  cities.splice(index, 1)
  delete cityCoords[cityName]
  updateCitiesEditor()
  drawCities()
}

function handleCSVUpload(event) {
  const file = event.target.files[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const content = e.target.result
      const lines = content.split("\n").filter((line) => line.trim())

      // Skip header
      const dataLines = lines.slice(1)

      if (dataLines.length < 3) {
        alert("File CSV phải có ít nhất 3 thành phố!")
        return
      }

      // Parse CSV
      const newCities = []
      const newCoords = {}

      dataLines.forEach((line) => {
        const parts = line.split(",").map((p) => p.trim())
        if (parts.length >= 3) {
          const name = parts[0]
          const lon = Number.parseFloat(parts[1])
          const lat = Number.parseFloat(parts[2])

          if (name && !isNaN(lon) && !isNaN(lat)) {
            newCities.push(name)
            newCoords[name] = [lon, lat]
          }
        }
      })

      if (newCities.length < 3) {
        alert("Không thể đọc đủ dữ liệu từ file CSV!")
        return
      }

      // Update data
      cities = newCities
      cityCoords = newCoords

      // Show info
      const csvInfo = document.getElementById("csvInfo")
      csvInfo.style.display = "block"
      csvInfo.innerHTML = `
                <strong style="color: #7fff00;">✅ Đã tải file thành công!</strong><br>
                📁 File: ${file.name}<br>
                🏙️ Số thành phố: ${cities.length}
            `

      // Update display
      updateCitiesList()
      drawCities()
    } catch (error) {
      alert("Lỗi khi đọc file CSV: " + error.message)
    }
  }

  reader.readAsText(file)
}

async function solveTSP() {
  if (cities.length < 3) {
    alert("Cần ít nhất 3 thành phố để giải bài toán TSP!")
    return
  }

  const solveBtn = document.getElementById("solveBtn")
  const compareBtn = document.getElementById("compareBtn")
  const resultsBox = document.getElementById("resultsBox")
  const loadingIndicator = document.getElementById("loadingIndicator")

  solveBtn.disabled = true
  compareBtn.disabled = true
  loadingIndicator.classList.add("active")
  resultsBox.innerHTML = '<div style="color: #f7d046;">Đang giải bài toán...</div>'

  const params = {
    cities: cities,
    coords: cityCoords,
    n_ants: Number.parseInt(document.getElementById("nAnts").value),
    n_iterations: Number.parseInt(document.getElementById("nIterations").value),
    alpha: Number.parseFloat(document.getElementById("alpha").value),
    beta: Number.parseFloat(document.getElementById("beta").value),
    evaporation: Number.parseFloat(document.getElementById("evaporation").value),
    q: Number.parseFloat(document.getElementById("q").value),
  }

  try {
    const response = await fetch("/solve", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(params),
    })

    if (!response.ok) {
      throw new Error("Lỗi khi giải bài toán")
    }

    results = await response.json()

    // Hiển thị kết quả
    let output = "=".repeat(50) + "\n"
    output += "THUẬT TOÁN BACKTRACKING (simpleAI)\n"
    output += "=".repeat(50) + "\n\n"
    output += `Tuyến đường: ${results.backtracking.route.join(" → ")} → ${results.backtracking.route[0]}\n`
    output += `Tổng khoảng cách: ${results.backtracking.distance.toFixed(2)} km\n`
    output += `Thời gian: ${results.backtracking.time.toFixed(4)} giây\n\n`

    output += "=".repeat(50) + "\n"
    output += "THUẬT TOÁN ACO (Ant Colony Optimization)\n"
    output += "=".repeat(50) + "\n\n"
    output += `Tuyến đường: ${results.aco.route.join(" → ")} → ${results.aco.route[0]}\n`
    output += `Tổng khoảng cách: ${results.aco.distance.toFixed(2)} km\n`
    output += `Thời gian: ${results.aco.time.toFixed(4)} giây\n\n`

    output += "=".repeat(50) + "\n"
    output += '✅ Hoàn thành! Nhấn "So sánh kết quả" để xem chi tiết.\n'
    output += "=".repeat(50)

    resultsBox.innerHTML = `<pre style="margin: 0; white-space: pre-wrap;">${output}</pre>`

    // Vẽ kết quả
    drawRoute("backtrackingCanvas", results.backtracking.route, "Backtracking", "#4a9eff")
    drawRoute("acoCanvas", results.aco.route, "ACO", "#ff6b6b")
    drawConvergence(results.aco.convergence)

    compareBtn.disabled = false
  } catch (error) {
    resultsBox.innerHTML = `<div style="color: #ff6b6b;">❌ Lỗi: ${error.message}</div>`
  } finally {
    loadingIndicator.classList.remove("active")
    solveBtn.disabled = false
  }
}

// Hiển thị so sánh
function showComparison() {
  if (!results.backtracking || !results.aco) {
    alert("Vui lòng giải bài toán trước!")
    return
  }

  const bt = results.backtracking
  const aco = results.aco

  const distanceWinner = bt.distance < aco.distance ? "Backtracking" : "ACO"
  const timeWinner = bt.time < aco.time ? "Backtracking" : "ACO"

  let conclusion = ""
  if (bt.distance < aco.distance) {
    conclusion = `✅ Backtracking tìm được tuyến đường ngắn hơn (${bt.distance.toFixed(2)} km so với ${aco.distance.toFixed(2)} km)\n⏱️ Tuy nhiên, ACO có thể nhanh hơn với bài toán lớn và cho kết quả gần tối ưu`
  } else if (aco.distance < bt.distance) {
    conclusion = `✅ ACO tìm được tuyến đường ngắn hơn (${aco.distance.toFixed(2)} km so với ${bt.distance.toFixed(2)} km)\n⚡ ACO phù hợp hơn cho bài toán TSP với nhiều thành phố`
  } else {
    conclusion = "🤝 Cả hai thuật toán đều tìm được tuyến đường có độ dài bằng nhau"
  }

  const comparisonHTML = `
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 1000;" onclick="this.remove()">
            <div style="background: #1a1a1a; border-radius: 16px; padding: 40px; max-width: 900px; width: 90%; border: 1px solid rgba(247, 208, 70, 0.2);" onclick="event.stopPropagation()">
                <h2 style="color: #f7d046; margin-bottom: 30px; text-align: center;">📊 SO SÁNH KẾT QUẢ</h2>
                
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Tiêu chí</th>
                            <th>Backtracking</th>
                            <th>ACO</th>
                            <th>Tốt hơn</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Khoảng cách (km)</td>
                            <td class="${distanceWinner === "Backtracking" ? "winner" : ""}">${bt.distance.toFixed(2)}</td>
                            <td class="${distanceWinner === "ACO" ? "winner" : ""}">${aco.distance.toFixed(2)}</td>
                            <td style="color: #f7d046; font-weight: 600;">${distanceWinner}</td>
                        </tr>
                        <tr>
                            <td>Thời gian (giây)</td>
                            <td class="${timeWinner === "Backtracking" ? "winner" : ""}">${bt.time.toFixed(4)}</td>
                            <td class="${timeWinner === "ACO" ? "winner" : ""}">${aco.time.toFixed(4)}</td>
                            <td style="color: #f7d046; font-weight: 600;">${timeWinner}</td>
                        </tr>
                        <tr>
                            <td>Số thành phố</td>
                            <td>${cities.length}</td>
                            <td>${cities.length}</td>
                            <td style="color: #999;">Bằng nhau</td>
                        </tr>
                    </tbody>
                </table>

                <div style="background: rgba(247, 208, 70, 0.05); border: 1px solid rgba(247, 208, 70, 0.2); border-radius: 8px; padding: 20px; margin-top: 30px;">
                    <h3 style="color: #f7d046; margin-bottom: 12px;">📝 KẾT LUẬN</h3>
                    <p style="line-height: 1.8; white-space: pre-line;">${conclusion}</p>
                </div>

                <button class="btn btn-primary" style="margin-top: 30px;" onclick="this.closest('div[style*=fixed]').remove()">
                    Đóng
                </button>
            </div>
        </div>
    `

  document.body.insertAdjacentHTML("beforeend", comparisonHTML)
}

// Vẽ vị trí các thành phố ban đầu
function drawCities() {
  const canvas = document.getElementById("citiesCanvas")
  const ctx = canvas.getContext("2d")
  const width = (canvas.width = canvas.offsetWidth)
  const height = (canvas.height = canvas.offsetHeight)

  ctx.fillStyle = "#2a2a2a"
  ctx.fillRect(0, 0, width, height)

  // Tính toán scale
  const lons = cities.map((c) => cityCoords[c][0])
  const lats = cities.map((c) => cityCoords[c][1])
  const minLon = Math.min(...lons)
  const maxLon = Math.max(...lons)
  const minLat = Math.min(...lats)
  const maxLat = Math.max(...lats)

  const padding = 60
  const scaleX = (width - 2 * padding) / (maxLon - minLon)
  const scaleY = (height - 2 * padding) / (maxLat - minLat)

  // Vẽ các thành phố
  cities.forEach((city) => {
    const [lon, lat] = cityCoords[city]
    const x = padding + (lon - minLon) * scaleX
    const y = height - (padding + (lat - minLat) * scaleY)

    // Vẽ điểm
    ctx.beginPath()
    ctx.arc(x, y, 8, 0, 2 * Math.PI)
    ctx.fillStyle = "#f7d046"
    ctx.fill()
    ctx.strokeStyle = "#fff"
    ctx.lineWidth = 2
    ctx.stroke()

    // Vẽ tên thành phố
    ctx.fillStyle = "#fff"
    ctx.font = "bold 11px Arial"
    ctx.fillText(city, x + 12, y + 4)
  })
}

// Vẽ tuyến đường
function drawRoute(canvasId, route, title, color = "#f7d046") {
  const canvas = document.getElementById(canvasId)
  const ctx = canvas.getContext("2d")
  const width = (canvas.width = canvas.offsetWidth)
  const height = (canvas.height = canvas.offsetHeight)

  ctx.fillStyle = "#2a2a2a"
  ctx.fillRect(0, 0, width, height)

  if (!route || route.length === 0) {
    ctx.fillStyle = "#666"
    ctx.font = "14px Arial"
    ctx.textAlign = "center"
    ctx.fillText("Chờ kết quả...", width / 2, height / 2)
    return
  }

  // Tính toán scale
  const lons = cities.map((c) => cityCoords[c][0])
  const lats = cities.map((c) => cityCoords[c][1])
  const minLon = Math.min(...lons)
  const maxLon = Math.max(...lons)
  const minLat = Math.min(...lats)
  const maxLat = Math.max(...lats)

  const padding = 60
  const scaleX = (width - 2 * padding) / (maxLon - minLon)
  const scaleY = (height - 2 * padding) / (maxLat - minLat)

  // Vẽ đường nối
  ctx.beginPath()
  route.forEach((city, i) => {
    const [lon, lat] = cityCoords[city]
    const x = padding + (lon - minLon) * scaleX
    const y = height - (padding + (lat - minLat) * scaleY)

    if (i === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })

  // Quay về điểm xuất phát
  const [lon0, lat0] = cityCoords[route[0]]
  const x0 = padding + (lon0 - minLon) * scaleX
  const y0 = height - (padding + (lat0 - minLat) * scaleY)
  ctx.lineTo(x0, y0)

  ctx.strokeStyle = color
  ctx.lineWidth = 2
  ctx.stroke()

  // Vẽ các điểm
  route.forEach((city, i) => {
    const [lon, lat] = cityCoords[city]
    const x = padding + (lon - minLon) * scaleX
    const y = height - (padding + (lat - minLat) * scaleY)

    ctx.beginPath()
    ctx.arc(x, y, 6, 0, 2 * Math.PI)
    ctx.fillStyle = color
    ctx.fill()
    ctx.strokeStyle = "#fff"
    ctx.lineWidth = 2
    ctx.stroke()

    // Vẽ số thứ tự
    ctx.fillStyle = "#fff"
    ctx.font = "bold 10px Arial"
    ctx.fillText((i + 1).toString(), x + 10, y - 10)
  })
}

// Vẽ biểu đồ hội tụ
function drawConvergence(convergenceData) {
  const canvas = document.getElementById("convergenceCanvas")
  const ctx = canvas.getContext("2d")
  const width = (canvas.width = canvas.offsetWidth)
  const height = (canvas.height = canvas.offsetHeight)

  ctx.fillStyle = "#2a2a2a"
  ctx.fillRect(0, 0, width, height)

  if (!convergenceData || convergenceData.length === 0) {
    ctx.fillStyle = "#666"
    ctx.font = "14px Arial"
    ctx.textAlign = "center"
    ctx.fillText("Chờ kết quả...", width / 2, height / 2)
    return
  }

  const padding = 50
  const graphWidth = width - 2 * padding
  const graphHeight = height - 2 * padding

  const maxValue = Math.max(...convergenceData)
  const minValue = Math.min(...convergenceData)
  const valueRange = maxValue - minValue

  // Vẽ trục
  ctx.strokeStyle = "#666"
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(padding, padding)
  ctx.lineTo(padding, height - padding)
  ctx.lineTo(width - padding, height - padding)
  ctx.stroke()

  // Vẽ đường hội tụ
  ctx.beginPath()
  convergenceData.forEach((value, i) => {
    const x = padding + (i / (convergenceData.length - 1)) * graphWidth
    const y = height - padding - ((value - minValue) / valueRange) * graphHeight

    if (i === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })

  ctx.strokeStyle = "#f7d046"
  ctx.lineWidth = 2
  ctx.stroke()

  // Vẽ nhãn
  ctx.fillStyle = "#fff"
  ctx.font = "11px Arial"
  ctx.fillText("Iteration", width / 2, height - 10)
  ctx.save()
  ctx.translate(15, height / 2)
  ctx.rotate(-Math.PI / 2)
  ctx.fillText("Khoảng cách (km)", 0, 0)
  ctx.restore()
}

// Khởi tạo
window.addEventListener("load", () => {
  updateCitiesList()
  drawCities()
  drawRoute("backtrackingCanvas", null, "Backtracking")
  drawRoute("acoCanvas", null, "ACO")
  drawConvergence(null)
})

window.addEventListener("resize", () => {
  drawCities()
  if (results.backtracking) {
    drawRoute("backtrackingCanvas", results.backtracking.route, "Backtracking", "#4a9eff")
  }
  if (results.aco) {
    drawRoute("acoCanvas", results.aco.route, "ACO", "#ff6b6b")
    drawConvergence(results.aco.convergence)
  }
})
