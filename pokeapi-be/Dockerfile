FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first for better caching
COPY package.json ./
COPY yarn.lock ./

# Install dependencies including devDependencies
RUN yarn install --frozen-lockfile

# Copy all files
COPY . .

# Build the app
RUN yarn build

# Remove dev dependencies
RUN yarn install --production --ignore-scripts --prefer-offline

FROM node:20-alpine AS runner

WORKDIR /app

# Copy built app and production dependencies
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Use non-root user
USER node

# Start the app
CMD ["node", "dist/main.js"]



# FROM node:20-alpine AS builder

# WORKDIR /app

# COPY package.json ./
# COPY yarn.lock ./

# RUN yarn install

# COPY . .

# RUN yarn build

# FROM node:20-alpine AS runner

# WORKDIR /app
# COPY --from=builder --chown=node:node /app/dist ./dist
# COPY --from=builder --chown=node:node /app/node_modules ./node_modules

# ENV NODE_ENV=production
# USER node

# CMD ["node", "dist/main.js"]