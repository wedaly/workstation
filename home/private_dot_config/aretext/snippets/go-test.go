func Test<NAME>(t *testing.T) {
	testCases := []struct{
		name string
	}{
		{
			name: "<name>",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// <test>
		})
	}
}
