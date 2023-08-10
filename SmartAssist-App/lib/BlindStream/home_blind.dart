import 'package:flutter/material.dart';
import 'package:flutter_vlc_player/flutter_vlc_player.dart';

import '../utils/colors.dart';

class LiveStream extends StatefulWidget {
  @override
  _LiveStreamState createState() => _LiveStreamState();
}

class _LiveStreamState extends State<LiveStream> {
  late VlcPlayerController _vlcController;
  final String _url = "http://192.168.137.204:8081/";

  @override
  void initState() {
    super.initState();
    _initVlcPlayer();
  }

  @override
  void dispose() {
    _vlcController.dispose();
    super.dispose();
  }

  void _initVlcPlayer() {
    _vlcController = VlcPlayerController.network(_url);
    _vlcController.initialize();
    _vlcController.play();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        backgroundColor: secondaryColor,
        elevation: 0,
        toolbarHeight: 80,
        title: Text(
          'Live Stream',
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.bold,
          ),
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.only(
            bottomLeft: Radius.circular(25),
            bottomRight: Radius.circular(25),
          ),
        ),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
              width: 400,
              height: 600,
              child: VlcPlayer(
                controller: _vlcController,
                aspectRatio: 4 / 3,
                placeholder: Container(
                  child: CircularProgressIndicator(),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
