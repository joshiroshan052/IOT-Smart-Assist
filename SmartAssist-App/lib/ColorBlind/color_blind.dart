import 'package:flutter/material.dart';
import 'package:tflite/tflite.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import '../utils/colors.dart';
import 'tts.dart';

class ColorRecognition extends StatefulWidget {
  @override
  _ColorRecognitionState createState() => _ColorRecognitionState();
}

class _ColorRecognitionState extends State<ColorRecognition> {
  File? _image;
  List? _outputs;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _loading = true;
    speak('Click anywhere to open the camera and take a photo');
    loadModel().then((value) {
      setState(() {
        _loading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Color Recognition',
          style: TextStyle(
            fontFamily: 'nerko',
            fontSize: 30,
            color: Colors.white,
          ),
        ),
        backgroundColor: secondaryColor,
        elevation: 0,
        toolbarHeight: 80,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.only(
            bottomLeft: Radius.circular(25),
            bottomRight: Radius.circular(25),
          ),
        ),
      ),
      body: _loading
          ? Container(
        alignment: Alignment.center,
        child: CircularProgressIndicator(),
      )
          : Container(
        color: Colors.white,
        width: MediaQuery.of(context).size.width,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _image == null
                ? Expanded(
              child: GestureDetector(
                onTap: pickImage,
                child: Container(
                  height: double.infinity,
                  width: double.infinity,
                  color: Colors.white,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'Click anywhere to open the Camera',
                        style: TextStyle(
                            color: Colors.black,
                            fontSize: 30,
                            fontFamily: 'nerko'),
                      ),
                    ],
                  ),
                ),
              ),
            )
                : GestureDetector(
              onTap: () => Navigator.of(context).pop(),
              child: Column(
                children: [
                  Image.file(_image!),
                  const SizedBox(
                    height: 10,
                  ),
                  Text(
                    "This seems to be ${_outputs?[0]["label"].toString().substring(2)} color",
                    style: TextStyle(
                      color: Colors.red,
                      fontFamily: 'nerko',
                      fontSize: 30,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  pickImage() async {
    var image = await ImagePicker().getImage(source: ImageSource.camera);
    if (image == null) return null;
    setState(() {
      _loading = true;
      _image = File(image.path);
    });
    classifyImage(_image!);
  }

  classifyImage(File image) async {
    var output = await Tflite.runModelOnImage(
      path: image.path,
      numResults: 2,
      threshold: 0.5,
      imageMean: 127.5,
      imageStd: 127.5,
    );
    setState(() {
      _loading = false;
      _outputs = output;
    });
    if (_outputs != null) {
      speak("This seems to be ${_outputs?[0]["label"].toString().substring(2)} color. Click anywhere to start again.");
    }
  }

  loadModel() async {
    await Tflite.loadModel(
      model: "assets/model/model_unquant2.tflite",
      labels: "assets/model/labels2.txt",
    );
  }


  @override
  void dispose() {
    Tflite.close();
    super.dispose();
  }
}
