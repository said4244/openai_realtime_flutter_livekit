import 'package:flutter/material.dart';
import 'package:livekit_voice_assistant/livekit_voice_assistant.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice Assistant Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const VoiceAssistantDemo(),
    );
  }
}

class VoiceAssistantDemo extends StatefulWidget {
  const VoiceAssistantDemo({super.key});

  @override
  State<VoiceAssistantDemo> createState() => _VoiceAssistantDemoState();
}

class _VoiceAssistantDemoState extends State<VoiceAssistantDemo> {
  late final VoiceAssistant assistant;
  bool isActive = false;

  @override
  void initState() {
    super.initState();
    
    // That's it! Just configure and create the assistant
    assistant = VoiceAssistant(
      config: VoiceAssistantConfig(
        tokenUrl: 'http://localhost:8080/token',  // Replace with your token server
        enableLogging: true,  // See all the logs in console
      ),
    );

    // Listen to status updates (optional)
    assistant.statusStream.listen((status) {
      debugPrint('Status: $status');
    });
  }

  @override
  void dispose() {
    assistant.dispose();
    super.dispose();
  }

  void _toggleAssistant() async {
    if (!isActive) {
      await assistant.start();
    } else {
      await assistant.stop();
    }
    
    setState(() {
      isActive = !isActive;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: GestureDetector(
          onTap: _toggleAssistant,
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            width: 200,
            height: 200,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: isActive ? Colors.red : Colors.green,
              boxShadow: [
                BoxShadow(
                  color: (isActive ? Colors.red : Colors.green).withOpacity(0.5),
                  blurRadius: isActive ? 30 : 10,
                  spreadRadius: isActive ? 10 : 5,
                ),
              ],
            ),
            child: Icon(
              isActive ? Icons.stop : Icons.mic,
              size: 80,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }
}