import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Map, Camera } from "@maplibre/maplibre-react-native";
import type { StyleSpecification } from "@maplibre/maplibre-react-native";

import mapStyleJson from "./assets/style.json";

const typedMapStyle = mapStyleJson as StyleSpecification;

export default function App() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Euskadi Transit - Mapa Local</Text>
      </View>
      <Map style={styles.map} mapStyle={typedMapStyle}>
        <Camera zoom={13} center={[-2.6724, 42.8467]} />
      </Map>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    height: 60,
    backgroundColor: "#111",
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 15,
  },
  headerText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "bold",
  },
  map: {
    flex: 1,
  },
});
