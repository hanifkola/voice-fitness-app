// /screens/HomeScreen.tsx
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const HomeScreen = ({ navigation }: any) => {
  const [workouts, setWorkouts] = useState<any[]>([]);

  useEffect(() => {
    const fetchWorkouts = async () => {
      const token = await AsyncStorage.getItem('@auth_token');
      try {
        const response = await axios.get('https://your-backend-url.com/workouts', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setWorkouts(response.data);
      } catch (error) {
        console.error('Error fetching workouts', error);
      }
    };

    fetchWorkouts();
  }, []);

  return (
    <View>
      <Text>Welcome to Voice Fitness App</Text>
      <FlatList
        data={workouts}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View>
            <Text>{item.exercise_name}</Text>
            <Text>{item.sets} sets, {item.reps} reps</Text>
          </View>
        )}
      />
      <Button title="Add Workout" onPress={() => navigation.navigate('AddWorkout')} />
    </View>
  );
};

export default HomeScreen;
