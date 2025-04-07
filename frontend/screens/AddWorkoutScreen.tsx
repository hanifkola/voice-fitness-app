// AddWorkoutScreen.tsx
import React, { useState } from 'react';
import { View, TextInput, Button } from 'react-native';
import axios from 'axios';

const AddWorkoutScreen = ({ navigation }: any) => {
  const [exerciseName, setExerciseName] = useState('');
  const [sets, setSets] = useState('');
  const [reps, setReps] = useState('');
  const [weight, setWeight] = useState('');

  const handleAddWorkout = async () => {
    const token = 'your-jwt-token'; // Get the token from AsyncStorage or SecureStore
    try {
      await axios.post('https://your-backend-url.com/workouts', {
        exercise_name: exerciseName,
        sets,
        reps,
        weight,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });
      navigation.goBack(); // Go back to Home after adding the workout
    } catch (error) {
      console.error('Error adding workout', error);
    }
  };

  return (
    <View>
      <TextInput
        value={exerciseName}
        onChangeText={setExerciseName}
        placeholder="Exercise Name"
      />
      <TextInput
        value={sets}
        onChangeText={setSets}
        placeholder="Sets"
        keyboardType="numeric"
      />
      <TextInput
        value={reps}
        onChangeText={setReps}
        placeholder="Reps"
        keyboardType="numeric"
      />
      <TextInput
        value={weight}
        onChangeText={setWeight}
        placeholder="Weight"
        keyboardType="numeric"
      />
      <Button title="Add Workout" onPress={handleAddWorkout} />
    </View>
  );
};

export default AddWorkoutScreen;
