export class WebSocketManager {
  private socket: WebSocket | null = null
  private readonly reconnectDelay = 5000
  private readonly serverUrl: string
  public onMessage: (message: any) => void
  private readonly onClose: () => void
  private readonly onError: () => void

  constructor(
    serverUrl: string,
    onMessage: (message: any) => void,
    onClose: () => void,
    onError: () => void
  ) {
    this.serverUrl = serverUrl
    this.onMessage = onMessage
    this.onClose = onClose
    this.onError = onError
  }

  public connect(): void {
    console.log(this.serverUrl)
    this.socket = new WebSocket(this.serverUrl)

    this.socket.addEventListener("open", () => {
      console.log(`Connected to the server at ${this.serverUrl}`)
    })

    this.socket.addEventListener("message", (event) => {
      try {
        const message = JSON.parse(event.data)
        this.onMessage(message)
      } catch (error) {
        console.error(`Error parsing message: ${error}`)
      }
    })

    this.socket.addEventListener("close", () => {
      console.log(`Disconnected from the server at ${this.serverUrl}`)
      this.onClose()
      this.attemptReconnect()
    })

    this.socket.addEventListener("error", (error) => {
      console.error(`WebSocket error: ${error}`)
      this.onError()
      this.socket?.close()
    })
  }

  private attemptReconnect(): void {
    setTimeout(() => this.connect(), this.reconnectDelay)
  }

  public send(data: any): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(data)
    } else {
      console.error("WebSocket is not open. Cannot send data.")
    }
  }

  public close(): void {
    if (this.socket) {
      this.socket.close()
    }
  }

  public setOnMessage(callback: (message: any) => void): void {
    this.onMessage = callback
  }
}