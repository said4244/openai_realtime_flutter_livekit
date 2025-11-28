# LiveKit Voice Assistant

A Flutter package that simplifies integration of real-time voice AI assistants using LiveKit and OpenAI's Realtime API.

## Prerequisites

- LiveKit server access (can use LiveKit Cloud or self-hosted)
- OpenAI API key with Realtime API access
- Flutter project ready for voice integration
- Python for running the agent server

## Installation

1. Add the package to your `pubspec.yaml`:
```yaml
dependencies:
  livekit_voice_assistant: ^0.0.1
```

2. Clone the server components:
```bash
git clone <your-repo-url>
cd server
```

3. Create a `.env` file in the server directory:
```env
OPENAI_API_KEY=your_openai_api_key
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=wss://your-livekit-server.com
LOG_LEVEL=INFO
PORT=8080
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Start the Server Components

Run both server components (preferably in separate terminals):

```bash
# Terminal 1 - Token Server
python token_server.py

# Terminal 2 - AI Agent
python agent.py dev
```

### 2. Integrate in Flutter App

```dart
import 'package:livekit_voice_assistant/livekit_voice_assistant.dart';

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late final VoiceAssistant assistant;
  bool isActive = false;

  @override
  void initState() {
    super.initState();
    
    // Configure the assistant
    assistant = VoiceAssistant(
      config: VoiceAssistantConfig(
        tokenUrl: 'http://localhost:8080/token',  // Your token server URL
        enableLogging: true,
      ),
    );
  }

  // Start/Stop the assistant
  void toggleAssistant() async {
    if (!isActive) {
      await assistant.start();
    } else {
      await assistant.stop();
    }
    setState(() => isActive = !isActive);
  }

  @override
  void dispose() {
    assistant.dispose();
    super.dispose();
  }
}
```

## Configuration Options

### VoiceAssistantConfig
- `tokenUrl`: URL of your token server
- `livekitUrl`: (Optional) Custom LiveKit server URL
- `enableLogging`: Enable/disable debug logs
- `room`: (Optional) Custom room name

### Server Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `LIVEKIT_API_KEY`: LiveKit API key
- `LIVEKIT_API_SECRET`: LiveKit API secret  
- `LIVEKIT_URL`: LiveKit server WebSocket URL
- `LOG_LEVEL`: Server logging level (INFO, DEBUG, etc.)
- `PORT`: Token server port (default: 8080)

## Web Support

For web deployment, ensure:
1. Your token server uses HTTPS in production
2. CORS is properly configured if hosted on different domain
3. Microphone permissions are handled (package handles this automatically)

## Common Issues

1. **Connection Failed**: Check LiveKit credentials and server URL
2. **No Audio**: Verify microphone permissions and browser compatibility
3. **Token Error**: Ensure token server is running and URL is correct

## Production Deployment

1. Host token server behind HTTPS
2. Set proper CORS headers for your domain
3. Use environment variables for sensitive credentials
4. Consider rate limiting for token generation
5. Monitor server logs for issues

## License

MIT License - see LICENSE file

## Support

For issues and feature requests, please file them in the GitHub repository.
