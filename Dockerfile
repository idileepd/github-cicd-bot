# # Use an official Node.js runtime as a base image
# FROM node:14

# # Set the working directory in the container
# WORKDIR /app

# # Copy package.json and package-lock.json to the working directory
# COPY package*.json ./

# # Install app dependencies
# RUN npm install

# # Copy the application code to the container
# COPY . .

# Use a smaller base image suitable for production
FROM node:20-alpine


# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./


# Copy the rest of the application code to the working directory
COPY . .


# Remove existing node_modules and .next folders
RUN rm -rf node_modules dist .vscode

# Install project dependencies
RUN npm install


# Build the Next.js application
RUN npm run build

# Expose the port your app runs on
# EXPOSE 3000

# Command to run the application

CMD ["node", "./dist/server.js"]
