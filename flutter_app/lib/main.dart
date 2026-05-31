// BrailleVision -- app entry point. Place in lib/ alongside braille_screen.dart.
import 'package:flutter/material.dart';
import 'braille_screen.dart';

void main() => runApp(const BrailleVisionApp());

class BrailleVisionApp extends StatelessWidget {
  const BrailleVisionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BrailleVision',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorSchemeSeed: Colors.indigo, useMaterial3: true),
      home: const BrailleScreen(),
    );
  }
}
