import { Drawer } from "expo-router/drawer";
import { Platform, Text, Slot, View } from "react-native";

export default function Layout() {
  if (Platform.OS === "web") {
    return <Text>Web</Text>;
  }

  return (
    <Drawer>
      <Drawer.Screen
        name="index"
        options={{
          drawerLabel: "Home",
          title: "Home",
        }}
      />
      <Drawer.Screen
        name="search"
        options={{
          drawerLabel: "Search",
          title: "Search",
        }}
      />
      <Drawer.Screen
        name="about"
        options={{
          drawerLabel: "About",
          title: "About",
        }}
      />
    </Drawer>
  );
}
